import { ThemeToggle } from "./theme-toggle"
import { Button } from "@/components/ui/button"

export function Navbar() {
    return (
        <nav className="w-full border-b bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-16 items-center justify-between mx-auto px-4">

                {/* LOGO */}
                <div className="text-xl font-bold">
                    MyApp
                </div>

                {/* MENU DIREITO */}
                <div className="flex items-center gap-4">
                    <Button variant="link">Home</Button>
                    <Button variant="link">Sobre</Button>

                    {/* TROCA DE TEMA */}
                    <ThemeToggle />
                </div>
            </div>
        </nav>
    )
}
