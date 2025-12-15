"use client"

import { useState } from "react"
import { Send, Sparkles, Brain, FileText, BarChart, Download, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

import { submitQuery } from "@/lib/api"

export default function Dashboard() {
  const [query, setQuery] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [activeStep, setActiveStep] = useState<string | null>(null)

  const [result, setResult] = useState<any>(null)

  const handleSearch = async () => {
    if (!query.trim()) return
    setIsProcessing(true)
    setResult(null)
    setActiveStep("determining_complexity")

    try {
      // Simulate steps for UI while waiting (since API is not streaming yet)
      const stepInterval = setInterval(() => {
        setActiveStep((current) => {
          if (current === "determining_complexity") return "planning"
          if (current === "planning") return "researching"
          if (current === "researching") return "analyzing"
          if (current === "analyzing") return "synthesizing"
          return "synthesizing"
        })
      }, 3000)

      const response = await submitQuery(query)
      clearInterval(stepInterval)

      setResult(response)
      setActiveStep(null)
    } catch (error) {
      console.error(error)
      // Fallback to mock for demo if API fails
      setTimeout(() => setActiveStep("research"), 1500)
      setTimeout(() => setActiveStep("analyzing"), 4000)
      setTimeout(() => setActiveStep("synthesizing"), 7000)
      setTimeout(() => {
        setActiveStep(null)
      }, 9000)
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight">Mission Control</h1>
        <p className="text-muted-foreground">
          Orchestrate multi-agent business intelligence workflows.
        </p>
      </div>

      {/* Query Input Area */}
      <Card className="border-2 border-primary/10 shadow-lg">
        <CardContent className="pt-6">
          <div className="flex gap-4">
            <Textarea
              placeholder="Ask a complex business question (e.g., 'Analyze the competitive landscape for AI agents in 2025 and propose a pricing strategy')..."
              className="resize-none min-h-[100px] text-lg p-4"
              value={query}
              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setQuery(e.target.value)}
              onKeyDown={(e: React.KeyboardEvent<HTMLTextAreaElement>) => e.key === "Enter" && !e.shiftKey && handleSearch()}
            />
          </div>
        </CardContent>
        <CardFooter className="bg-muted/30 px-6 py-4 flex justify-between items-center">
          <div className="flex gap-2">
            <Badge variant="outline" className="bg-background">
              <Sparkles className="w-3 h-3 mr-1 text-yellow-500" />
              GPT-5 Enabled
            </Badge>
            <Badge variant="outline" className="bg-background">
              <Brain className="w-3 h-3 mr-1 text-blue-500" />
              DeepSeek R1
            </Badge>
          </div>
          <Button size="lg" onClick={handleSearch} disabled={isProcessing} className="px-8">
            {isProcessing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Orchestrating Agents...
              </>
            ) : (
              <>
                <Send className="mr-2 h-4 w-4" />
                Initialize Agents
              </>
            )}
          </Button>
        </CardFooter>
      </Card>

      {/* Output Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Left Column: Live Agent Status */}
        <div className="space-y-6">
          <Card className="h-full">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ActivityIcon />
                Live Agent Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6 relative pl-4 border-l-2 border-muted">
                <StatusItem
                  title="Query Classifier"
                  status={activeStep ? "completed" : "idle"}
                  description="Determining complexity..."
                />
                <StatusItem
                  title="Agent Router"
                  status={activeStep === "planning" ? "active" : (activeStep ? "completed" : "idle")}
                  description="Selecting specialized agents..."
                />
                <StatusItem
                  title="Research Synthesis"
                  status={activeStep === "research" ? "active" : (["analyzing", "synthesizing"].includes(activeStep || "") ? "completed" : "idle")}
                  description="Retrieving academic papers..."
                />
                <StatusItem
                  title="Parallel Execution"
                  status={activeStep === "analyzing" ? "active" : (activeStep === "synthesizing" ? "completed" : "idle")}
                  description="Running 4 agents concurrently..."
                />
                <StatusItem
                  title="Final Synthesis"
                  status={activeStep === "synthesizing" ? "active" : "idle"}
                  description="Compiling deliverable deck..."
                />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Results & Artifacts */}
        <div className="lg:col-span-2 space-y-6">
          <Tabs defaultValue="report" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="report">Executive Report</TabsTrigger>
              <TabsTrigger value="artifacts">Deliverables</TabsTrigger>
              <TabsTrigger value="logs">System Logs</TabsTrigger>
            </TabsList>

            <TabsContent value="report" className="mt-4">
              <Card>
                <CardHeader>
                  <CardTitle>Executive Summary</CardTitle>
                  <CardDescription>
                    Synthesized from Market Analysis, Financial Modeling, and Operations Audit.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {!result && !activeStep && !isProcessing ? (
                    <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
                      <Brain className="h-12 w-12 mb-4 opacity-20" />
                      <p>Enter a query to begin analysis</p>
                    </div>
                  ) : isProcessing ? (
                    <div className="prose dark:prose-invert max-w-none">
                      <div className="h-4 bg-muted rounded w-3/4 mb-4 animate-pulse" />
                      <div className="h-4 bg-muted rounded w-full mb-2 animate-pulse" />
                      <div className="h-4 bg-muted rounded w-5/6 mb-8 animate-pulse" />
                      <div className="h-32 bg-muted/50 rounded-lg flex items-center justify-center border border-dashed">
                        <span className="text-muted-foreground text-sm">Waiting for agents...</span>
                      </div>
                    </div>
                  ) : result ? (
                    <ScrollArea className="h-[400px] pr-4">
                      <div className="prose dark:prose-invert max-w-none">
                        <div className="whitespace-pre-wrap text-sm leading-relaxed">
                          {result.recommendation}
                        </div>
                        {result.agents_consulted && result.agents_consulted.length > 0 && (
                          <div className="flex gap-2 mt-4 flex-wrap">
                            <span className="text-xs text-muted-foreground">Agents Consulted:</span>
                            {result.agents_consulted.map((agent: string) => (
                              <Badge key={agent} variant="secondary" className="text-xs">{agent}</Badge>
                            ))}
                          </div>
                        )}
                      </div>
                    </ScrollArea>
                  ) : null}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="artifacts" className="mt-4">
              <div className="grid grid-cols-2 gap-4">
                <ArtifactCard
                  title="Strategic Analysis Deck"
                  type="PPTX"
                  size="2.4 MB"
                  icon={<FileText className="h-8 w-8 text-orange-500" />}
                />
                <ArtifactCard
                  title="Financial Model"
                  type="XLSX"
                  size="850 KB"
                  icon={<BarChart className="h-8 w-8 text-green-500" />}
                />
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}

function StatusItem({ title, status, description }: { title: string, status: "idle" | "active" | "completed", description: string }) {
  return (
    <div className={`relative ${status === "idle" ? "opacity-40" : "opacity-100"} transition-all duration-500`}>
      <div className={`absolute -left-[21px] top-1 h-4 w-4 rounded-full border-2 
        ${status === "completed" ? "bg-green-500 border-green-500" :
          status === "active" ? "bg-background border-primary animate-pulse" : "bg-background border-muted"}`}
      />
      <div>
        <h4 className={`font-medium text-sm ${status === "active" ? "text-primary" : ""}`}>{title}</h4>
        <p className="text-xs text-muted-foreground">{description}</p>
      </div>
    </div>
  )
}

function ArtifactCard({ title, type, size, icon }: any) {
  return (
    <Card className="hover:bg-muted/50 transition-colors cursor-pointer group">
      <CardContent className="p-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="p-2 bg-background rounded-lg shadow-sm group-hover:shadow-md transition-all">
            {icon}
          </div>
          <div>
            <h4 className="font-semibold">{title}</h4>
            <p className="text-xs text-muted-foreground">{type} • {size}</p>
          </div>
        </div>
        <Button variant="ghost" size="icon">
          <Download className="h-4 w-4" />
        </Button>
      </CardContent>
    </Card>
  )
}

function ActivityIcon() {
  return (
    <svg
      className=" h-4 w-4 text-muted-foreground"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
    </svg>
  )
}
