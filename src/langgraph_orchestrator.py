"""LangGraph-based orchestrator with state machine and parallel execution."""
import asyncio
from typing import Dict, Any, List, TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langsmith import traceable

from src.gpt5_wrapper import GPT5Wrapper
from src.agents.market_analysis import MarketAnalysisAgent
from src.agents.operations_audit import OperationsAuditAgent
from src.agents.financial_modeling import FinancialModelingAgent
from src.agents.lead_generation import LeadGenerationAgent
from src.agents.research_synthesis import ResearchSynthesisAgent
from src.tools.web_research import WebResearchTool
from src.memory import ConversationMemory
from src.config import Config


class AgentState(TypedDict):
    """State object passed between nodes in the graph."""
    query: str
    query_complexity: Literal["simple", "business", "complex"]
    agents_to_call: List[str]
    research_enabled: bool
    research_findings: Dict[str, Any]
    research_context: str
    market_analysis: str
    operations_audit: str
    financial_modeling: str
    lead_generation: str
    web_research: Dict[str, Any]
    synthesis: str
    conversation_history: List[Dict[str, str]]
    use_memory: bool


class LangGraphOrchestrator:
    """
    LangGraph-based orchestrator with state machine routing.

    Architecture:
        User Query → Router Node → Parallel Agent Execution → Synthesis Node → Result
    """

    def __init__(self, enable_rag: bool = True, use_ml_routing: bool = False):
        """
        Initialize the LangGraph Orchestrator.

        Args:
            enable_rag: Enable research-augmented generation (default: True)
            use_ml_routing: Use ML classifier for routing instead of GPT-5 (default: False)
        """
        self.gpt5 = GPT5Wrapper()
        self.enable_rag = enable_rag
        self.use_ml_routing = use_ml_routing

        # Initialize agents
        self.market_agent = MarketAnalysisAgent()
        self.operations_agent = OperationsAuditAgent()
        self.financial_agent = FinancialModelingAgent()
        self.lead_gen_agent = LeadGenerationAgent()

        # Initialize research agent (RAG)
        if self.enable_rag:
            self.research_agent = ResearchSynthesisAgent()
            print("✓ RAG enabled - Research Synthesis Agent initialized")
        else:
            self.research_agent = None
            print("⚠️  RAG disabled - Running without research augmentation")

        # Initialize ML routing classifier (if enabled)
        self.ml_router = None
        if self.use_ml_routing:
            try:
                import os
                if os.path.exists("models/routing_classifier.pkl"):
                    from src.ml.routing_classifier import RoutingClassifier
                    self.ml_router = RoutingClassifier()
                    self.ml_router.load("models/routing_classifier.pkl")
                    print("✓ ML routing enabled - Classifier loaded")
                else:
                    print("⚠️  ML routing requested but model not found. Using GPT-5 routing.")
                    self.use_ml_routing = False
            except Exception as e:
                print(f"⚠️  ML routing failed to load: {e}. Using GPT-5 routing.")
                self.use_ml_routing = False

        if not self.use_ml_routing:
            print("✓ Using GPT-5 semantic routing")

        # Initialize tools
        self.web_research = WebResearchTool()

        # Initialize memory
        self.memory = ConversationMemory(max_messages=Config.MAX_MEMORY_MESSAGES)

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state machine with conditional routing."""
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("complexity_classifier", self._complexity_classifier_node)
        workflow.add_node("fast_answer", self._fast_answer_node)
        workflow.add_node("router", self._router_node)

        # Add research synthesis node (always add, but it's a no-op if RAG disabled)
        workflow.add_node("research_synthesis", self._research_synthesis_node)

        # Add parallel agent execution node
        workflow.add_node("parallel_agents", self._parallel_agents_node)
        workflow.add_node("synthesis", self._synthesis_node)

        # Set entry point
        workflow.set_entry_point("complexity_classifier")

        # Conditional routing based on query complexity
        workflow.add_conditional_edges(
            "complexity_classifier",
            self._route_by_complexity,
            {
                "simple": "fast_answer",
                "business": "router",
                "complex": "router",
            }
        )

        # Fast answer goes directly to END
        workflow.add_edge("fast_answer", END)

        # Router goes to research (if complex) or directly to agents
        workflow.add_conditional_edges(
            "router",
            self._route_after_router,
            {
                "research": "research_synthesis",
                "agents": "parallel_agents",
            }
        )

        # Research synthesis → parallel agents (always exists, but may be no-op)
        workflow.add_edge("research_synthesis", "parallel_agents")

        # Parallel agents → synthesis
        workflow.add_edge("parallel_agents", "synthesis")

        # Synthesis is the end
        workflow.add_edge("synthesis", END)

        return workflow.compile()

    @traceable(name="complexity_classifier")
    def _complexity_classifier_node(self, state: AgentState) -> AgentState:
        """
        Classify query complexity to determine routing strategy.

        - simple: Non-business questions (e.g., "what's the color of the sky") → fast answer
        - business: Business queries that don't need research (e.g., "improve retention") → agents only
        - complex: Complex business queries that benefit from research → research + agents
        """
        query = state["query"]

        classification_prompt = f"""Classify this query's complexity for a business intelligence system:

Query: {query}

Categories:
- simple: Non-business questions, general knowledge, casual conversation (answer in <3 seconds)
- business: Business questions that can be answered by our agents without research papers
- complex: Deep business questions requiring academic research backing

Respond with ONLY ONE WORD: simple, business, or complex

Examples:
"What's the color of the sky?" → simple
"How do I improve customer retention?" → business
"What's the optimal pricing strategy for B2B SaaS with 500+ customers based on latest research?" → complex

Classification:"""

        try:
            response = self.gpt5.generate(
                input_text=classification_prompt,
                reasoning_effort="low",
                text_verbosity="low",
            ).strip().lower()

            # Extract classification
            if "simple" in response:
                complexity = "simple"
            elif "complex" in response:
                complexity = "complex"
            elif "business" in response:
                complexity = "business"
            else:
                # Default to business if unclear
                complexity = "business"

            print(f"🔍 Query Complexity: {complexity.upper()}")
            state["query_complexity"] = complexity

        except Exception as e:
            print(f"⚠️  Complexity classification failed: {e}, defaulting to 'business'")
            state["query_complexity"] = "business"

        return state

    def _route_by_complexity(self, state: AgentState) -> str:
        """Route based on query complexity."""
        complexity = state.get("query_complexity", "business")
        return complexity

    @traceable(name="fast_answer")
    def _fast_answer_node(self, state: AgentState) -> AgentState:
        """
        Fast direct answer for simple non-business queries.
        Bypasses all agents for <3 second response time.
        """
        query = state["query"]

        print("⚡ Fast Answer Mode - Direct response")

        # Use GPT-5 for simple, fast answer
        answer = self.gpt5.generate(
            input_text=f"Answer this question concisely:\n\n{query}",
            reasoning_effort="low",
            text_verbosity="medium",
        )

        state["synthesis"] = answer
        state["agents_to_call"] = []  # No agents needed

        return state

    def _route_after_router(self, state: AgentState) -> str:
        """Determine if research synthesis is needed after routing."""
        complexity = state.get("query_complexity", "business")

        # Only use research for COMPLEX queries (skip for business/simple)
        if complexity == "complex" and self.enable_rag:
            return "research"

        # Skip research for business and simple queries
        return "agents"

    @traceable(name="router_node")
    def _router_node(self, state: AgentState) -> AgentState:
        """
        Router node: Determines which agents to call based on query analysis.

        Uses ML classifier (if enabled) or GPT-5 for semantic routing.
        """
        query = state["query"]

        # Use ML routing if enabled
        if self.use_ml_routing and self.ml_router:
            try:
                # Define per-agent adaptive thresholds based on training performance
                # Market: Higher threshold (tends to over-predict)
                # Leadgen: Lower threshold (tends to under-predict)
                ADAPTIVE_THRESHOLDS = {
                    "market": 0.55,      # Slightly higher (80% multi-agent in training)
                    "financial": 0.45,   # Standard
                    "operations": 0.45,  # Standard
                    "leadgen": 0.35      # Lower (under-represented in training)
                }

                # Get predictions with adaptive thresholds
                agents_to_call = self.ml_router.predict(
                    query,
                    adaptive_thresholds=ADAPTIVE_THRESHOLDS
                )
                probas = self.ml_router.predict_proba(query)

                print(f"🤖 ML Router: {agents_to_call}")
                print(f"   Confidence: {probas}")

                # Confidence-based fallback logic
                # If ML is uncertain, fall back to GPT-5 for verification
                confidence_scores = list(probas.values())
                max_confidence = max(confidence_scores)
                min_confidence = min(confidence_scores)

                # Check for uncertainty indicators:
                # 1. All scores in the "muddy middle" (0.3-0.7)
                # 2. Very close scores (indecisive)
                # 3. No high-confidence predictions
                all_in_middle = all(0.3 <= score <= 0.7 for score in confidence_scores)
                max_spread = max_confidence - min_confidence
                indecisive = max_spread < 0.3  # All scores within 0.3 of each other

                if all_in_middle or (indecisive and max_confidence < 0.7):
                    print(f"⚠️  ML router uncertain (max={max_confidence:.2f}, spread={max_spread:.2f})")
                    print(f"   Falling back to GPT-5 for verification...")
                    # Fall through to GPT-5 routing
                else:
                    # ML is confident, use its prediction
                    print(f"   ✓ High confidence (max={max_confidence:.2f})")
                    state["agents_to_call"] = agents_to_call
                    return state

            except Exception as e:
                print(f"⚠️  ML routing failed: {e}, falling back to GPT-5")
                # Fall through to GPT-5 routing

        # Use GPT-5 to analyze which agents are needed
        routing_prompt = f"""Analyze the following business query and determine which specialized agents should be consulted.

Available agents:
- market: Market research, trends, competition, market sizing, customer segmentation
- operations: Process optimization, efficiency analysis, workflow improvement
- financial: Financial projections, ROI calculations, revenue/cost analysis, pricing
- leadgen: Customer acquisition, sales funnel, growth strategies, marketing

Query: {query}

Respond with a JSON array of agent names that should be consulted. For comprehensive business decisions, include multiple relevant agents.
Example: ["market", "financial", "leadgen"]

Only output the JSON array, nothing else."""

        try:
            response = self.gpt5.generate(
                input_text=routing_prompt,
                reasoning_effort="low",  # Low reasoning for fast routing
                text_verbosity="low",
            )

            # Parse agent list from response
            import json
            # Extract JSON array from response (handle potential markdown formatting)
            response_clean = response.strip().replace("```json", "").replace("```", "").strip()
            agents_to_call = json.loads(response_clean)

            # If no agents selected, use all for comprehensive analysis
            if not agents_to_call:
                agents_to_call = ["market", "operations", "financial", "leadgen"]

            print(f"🧠 GPT-5 Router: {agents_to_call}")

        except Exception as e:
            print(f"Routing error: {e}, using all agents")
            # Fallback to all agents on error
            agents_to_call = ["market", "operations", "financial", "leadgen"]

        state["agents_to_call"] = agents_to_call
        return state

    @traceable(name="research_synthesis")
    def _research_synthesis_node(self, state: AgentState) -> AgentState:
        """
        Research synthesis node: Retrieves and synthesizes academic research.

        Only runs if RAG is enabled.
        """
        if not self.enable_rag or not self.research_agent:
            state["research_findings"] = {}
            state["research_context"] = ""
            return state

        query = state["query"]

        print("\n📚 Retrieving academic research...")

        try:
            # Retrieve and synthesize research
            research_result = self.research_agent.synthesize(
                query=query,
                retrieve_papers=True,
                top_k_papers=3
            )

            state["research_findings"] = research_result
            state["research_context"] = research_result.get("research_context", "")

            paper_count = research_result.get("paper_count", 0)
            if paper_count > 0:
                print(f"✓ Retrieved {paper_count} relevant papers")
                print(f"✓ Research synthesis complete")
            else:
                print("⚠️  No relevant research found - continuing without RAG")

        except Exception as e:
            print(f"⚠️  Research synthesis failed: {e}")
            print("   Continuing without research augmentation...")
            state["research_findings"] = {}
            state["research_context"] = ""

        return state

    @traceable(name="parallel_agents")
    def _parallel_agents_node(self, state: AgentState) -> AgentState:
        """
        Execute all required agents in parallel for 3x speedup.

        This replaces the old sequential execution chain.
        """
        agents_to_call = state.get("agents_to_call", [])

        if not agents_to_call:
            print("⚠️  No agents selected - skipping agent execution")
            return state

        print(f"🚀 Parallel Execution: {len(agents_to_call)} agents running concurrently")

        # Run agents in parallel using asyncio
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            state = loop.run_until_complete(self._execute_agents_parallel(state))
        finally:
            loop.close()

        print("✓ All agents completed")
        return state

    @traceable(name="synthesis_node")
    def _synthesis_node(self, state: AgentState) -> AgentState:
        """Synthesis node: Combines all agent outputs into final recommendation."""
        query = state["query"]

        # Collect agent outputs
        agent_outputs = []
        if state.get("market_analysis"):
            agent_outputs.append(f"MARKET ANALYSIS:\n{state['market_analysis']}")
        if state.get("operations_audit"):
            agent_outputs.append(f"OPERATIONS AUDIT:\n{state['operations_audit']}")
        if state.get("financial_modeling"):
            agent_outputs.append(f"FINANCIAL ANALYSIS:\n{state['financial_modeling']}")
        if state.get("lead_generation"):
            agent_outputs.append(f"LEAD GENERATION STRATEGY:\n{state['lead_generation']}")

        # If no agent outputs, return early (shouldn't happen, but safety check)
        if not agent_outputs:
            print("⚠️  No agent outputs to synthesize")
            state["synthesis"] = "No analysis available. Please try again."
            return state

        # If only one agent output, return it directly without synthesis overhead
        if len(agent_outputs) == 1:
            print("📝 Single agent output - skipping synthesis overhead")
            state["synthesis"] = agent_outputs[0]
            return state

        # Build synthesis prompt with conversation context
        context = ""
        if state.get("use_memory", True):
            context = f"\n\nConversation History:\n{self.memory.get_context_string()}\n\n"

        synthesis_prompt = f"""As the Business Intelligence Orchestrator, synthesize the following findings from specialized agents into a comprehensive, actionable recommendation.

Original Query: {query}
{context}
Agent Findings:

{chr(10).join(agent_outputs)}

Your task:
1. Identify key themes and insights across all agent analyses
2. Highlight any conflicts or trade-offs between recommendations
3. Provide a clear, prioritized action plan
4. Offer a holistic strategic recommendation

Provide an executive summary followed by detailed recommendations."""

        print(f"🔄 Synthesizing {len(agent_outputs)} agent outputs")

        synthesis = self.gpt5.generate(
            input_text=synthesis_prompt,
            reasoning_effort="low",  # Fixed: "high" uses all tokens for reasoning, no output
            text_verbosity="high",
        )

        state["synthesis"] = synthesis
        return state

    async def _execute_agents_parallel(
        self, state: AgentState
    ) -> AgentState:
        """Execute all required agents in parallel using asyncio."""
        agents_to_call = state.get("agents_to_call", [])

        # Create tasks for each agent
        tasks = []
        if "market" in agents_to_call:
            tasks.append(self._run_market_agent_async(state))
        if "operations" in agents_to_call:
            tasks.append(self._run_operations_agent_async(state))
        if "financial" in agents_to_call:
            tasks.append(self._run_financial_agent_async(state))
        if "leadgen" in agents_to_call:
            tasks.append(self._run_leadgen_agent_async(state))

        # Execute all agents in parallel
        results = await asyncio.gather(*tasks)

        # Update state with results
        for result in results:
            state.update(result)

        return state

    async def _run_market_agent_async(self, state: AgentState) -> Dict[str, str]:
        """Run market agent asynchronously in a thread pool."""
        # Use asyncio.to_thread to run blocking I/O in a separate thread
        loop = asyncio.get_event_loop()

        # Get web results (blocking I/O)
        web_results = state.get("web_research")
        if not web_results:
            web_results = await loop.run_in_executor(
                None, self.web_research.execute, state["query"]
            )

        research_context = state.get("research_context", "")

        # Run agent analysis (blocking I/O) in thread pool
        analysis = await loop.run_in_executor(
            None,
            lambda: self.market_agent.analyze(
                query=state["query"],
                web_research_results=web_results,
                research_context=research_context
            )
        )
        return {"market_analysis": analysis, "web_research": web_results}

    async def _run_operations_agent_async(self, state: AgentState) -> Dict[str, str]:
        """Run operations agent asynchronously in a thread pool."""
        loop = asyncio.get_event_loop()
        research_context = state.get("research_context", "")

        # Run agent audit (blocking I/O) in thread pool
        audit = await loop.run_in_executor(
            None,
            lambda: self.operations_agent.audit(
                query=state["query"],
                research_context=research_context
            )
        )
        return {"operations_audit": audit}

    async def _run_financial_agent_async(self, state: AgentState) -> Dict[str, str]:
        """Run financial agent asynchronously in a thread pool."""
        loop = asyncio.get_event_loop()
        research_context = state.get("research_context", "")

        # Run financial modeling (blocking I/O) in thread pool
        modeling = await loop.run_in_executor(
            None,
            lambda: self.financial_agent.model_financials(
                query=state["query"],
                research_context=research_context
            )
        )
        return {"financial_modeling": modeling}

    async def _run_leadgen_agent_async(self, state: AgentState) -> Dict[str, str]:
        """Run leadgen agent asynchronously in a thread pool."""
        loop = asyncio.get_event_loop()
        research_context = state.get("research_context", "")

        # Run lead gen strategy (blocking I/O) in thread pool
        strategy = await loop.run_in_executor(
            None,
            lambda: self.lead_gen_agent.generate_strategy(
                query=state["query"],
                research_context=research_context
            )
        )
        return {"lead_generation": strategy}

    @traceable(name="orchestrate_query")
    def orchestrate(self, query: str, use_memory: bool = True) -> Dict[str, Any]:
        """
        Orchestrate a business intelligence query using LangGraph.

        Args:
            query: User's business query
            use_memory: Whether to use conversation memory

        Returns:
            Dictionary containing detailed findings and synthesis
        """
        # Add to memory
        if use_memory:
            self.memory.add_message("user", query)

        # Initialize state
        initial_state: AgentState = {
            "query": query,
            "query_complexity": "business",  # Will be set by complexity classifier
            "agents_to_call": [],
            "research_enabled": self.enable_rag,
            "research_findings": {},
            "research_context": "",
            "market_analysis": "",
            "operations_audit": "",
            "financial_modeling": "",
            "lead_generation": "",
            "web_research": {},
            "synthesis": "",
            "conversation_history": self.memory.get_messages(),
            "use_memory": use_memory,
        }

        # Run the graph
        final_state = self.graph.invoke(initial_state)

        # Add synthesis to memory
        if use_memory:
            self.memory.add_message("assistant", final_state["synthesis"])

        # Return formatted results
        return {
            "query": query,
            "agents_consulted": final_state.get("agents_to_call", []),
            "detailed_findings": {
                "market_analysis": final_state.get("market_analysis", ""),
                "operations_audit": final_state.get("operations_audit", ""),
                "financial_modeling": final_state.get("financial_modeling", ""),
                "lead_generation": final_state.get("lead_generation", ""),
            },
            "recommendation": final_state["synthesis"],
        }

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.memory.get_messages()

    def clear_memory(self):
        """Clear the conversation memory."""
        self.memory.clear()
