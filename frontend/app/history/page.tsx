export default function HistoryPage() {
    return (
        <div className="space-y-6">
            <div className="flex flex-col gap-2">
                <h1 className="text-3xl font-bold tracking-tight">History</h1>
                <p className="text-muted-foreground">
                    View past agent interactions and generated reports.
                </p>
            </div>
            <div className="p-12 border rounded-lg border-dashed flex items-center justify-center text-muted-foreground bg-muted/20">
                No history available yet.
            </div>
        </div>
    )
}
