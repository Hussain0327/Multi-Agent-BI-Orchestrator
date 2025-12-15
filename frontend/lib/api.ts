const API_URL = "http://localhost:8000";

export interface QueryResponse {
    query: string;
    agents_consulted: string[];
    recommendation: string;
    detailed_findings: {
        market_analysis?: string;
        operations_audit?: string;
        financial_modeling?: string;
        lead_generation?: string;
    };
}

export async function submitQuery(query: string): Promise<QueryResponse> {
    const response = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
    });

    if (!response.ok) {
        throw new Error("Failed to fetch query results");
    }

    return response.json();
}

export async function getCacheStats() {
    const response = await fetch(`${API_URL}/cache/stats`);
    if (!response.ok) {
        throw new Error("Failed to fetch cache stats");
    }
    return response.json();
}
