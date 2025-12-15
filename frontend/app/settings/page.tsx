export default function SettingsPage() {
    return (
        <div className="space-y-6">
            <div className="flex flex-col gap-2">
                <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
                <p className="text-muted-foreground">
                    Configure agent behavior and API keys.
                </p>
            </div>
            <div className="p-12 border rounded-lg border-dashed flex items-center justify-center text-muted-foreground bg-muted/20">
                Settings validation requires admin access.
            </div>
        </div>
    )
}
