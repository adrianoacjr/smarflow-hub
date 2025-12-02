import { ReactNode } from "react"
import { Navbar } from "@/components/navbar"

export function MainLayout({ children }: { children: ReactNode}) {
    return (
        <div className="min-h-screen bg-background text-foreground">
            <Navbar />
            <main className="container mx-auto p-4"></main>
        </div>
    )
}
