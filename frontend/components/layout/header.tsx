export function Header() {
    return (
        <header className="flex h-16 items-center border-b px-6 bg-background/95 backdrop-blur z-10 sticky top-0">
            <div className="flex items-center gap-4">
                <h1 className="text-lg font-semibold">Dashboard</h1>
            </div>
            <div className="ml-auto flex items-center gap-4">
                <ModeToggle />
                <span className="text-sm text-muted-foreground">v2.0.0</span>
            </div>
        </header>
    )
}

import { ModeToggle } from "@/components/mode-toggle"
