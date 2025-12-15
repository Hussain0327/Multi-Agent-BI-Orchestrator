export default function CachePage() {
    return (
        <div className="space-y-6">
            <div className="flex flex-col gap-2">
                <h1 className="text-3xl font-bold tracking-tight">Cache Statistics</h1>
                <p className="text-muted-foreground">
                    Monitor Redis cache performance and cost savings.
                </p>
            </div>
            <div className="p-12 border rounded-lg border-dashed flex items-center justify-center text-muted-foreground bg-muted/20">
                Cache metrics loading...
            </div>
        </div>
    )
}
