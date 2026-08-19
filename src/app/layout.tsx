import type { Metadata, Viewport } from "next";
import "./globals.css";
import Link from "next/link";
import { 
  ShieldCheck, 
  HardHat, 
  LayoutDashboard, 
  Database, 
  AlertTriangle, 
  Calendar, 
  BarChart3 
} from "lucide-react";
import PWAProvider from "@/components/PWAProvider";

export const viewport: Viewport = {
  themeColor: "#16a34a",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export const metadata: Metadata = {
  title: "SGMC v2 — Transversal del Sisga",
  description: "Sistema de Gestión de Mantenimiento en Campo - Concesión Transversal del Sisga",
  manifest: "/manifest.json",
  icons: {
    icon: "/icon-192.png",
    apple: "/icon-192.png",
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "SGMC Sisga",
  },
  other: {
    "mobile-web-app-capable": "yes",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" className="dark">
      <body className="min-h-screen bg-slate-950 text-slate-100 flex flex-col antialiased">
        <PWAProvider />
        {/* Header Superior */}
        <header className="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-4 py-3">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-emerald-400 flex items-center justify-center shadow-lg shadow-emerald-900/40 group-hover:scale-105 transition-transform">
                <ShieldCheck className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-bold text-lg text-white tracking-tight">SGMC</span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-semibold border border-emerald-500/30">v2.0 Next</span>
                </div>
                <p className="text-xs text-slate-400 hidden sm:block">Concesión Transversal del Sisga</p>
              </div>
            </Link>

            {/* Navegación Principal */}
            <nav className="flex items-center gap-1 sm:gap-2">
              <Link
                href="/tecnico"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium bg-emerald-600 hover:bg-emerald-500 text-white shadow-md shadow-emerald-950 transition-all"
              >
                <HardHat className="w-4 h-4" />
                <span className="hidden sm:inline">Técnico</span>
              </Link>
              <Link
                href="/supervisor"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all"
              >
                <LayoutDashboard className="w-4 h-4 text-blue-400" />
                <span className="hidden sm:inline">Supervisor</span>
              </Link>
              <Link
                href="/novedades"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all"
              >
                <AlertTriangle className="w-4 h-4 text-amber-400" />
                <span className="hidden md:inline">Novedades</span>
              </Link>
              <Link
                href="/planes"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all"
              >
                <Calendar className="w-4 h-4 text-blue-400" />
                <span className="hidden md:inline">Planes</span>
              </Link>
              <Link
                href="/reportes"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all"
              >
                <BarChart3 className="w-4 h-4 text-emerald-400" />
                <span className="hidden md:inline">Reportes ($D_i$)</span>
              </Link>
              <Link
                href="/activos"
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all"
              >
                <Database className="w-4 h-4 text-amber-400" />
                <span className="hidden lg:inline">Activos (368)</span>
              </Link>
            </nav>
          </div>
        </header>

        {/* Contenido Principal */}
        <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
          {children}
        </main>

        {/* Footer */}
        <footer className="bg-slate-900 border-t border-slate-800 px-4 py-4 text-center text-xs text-slate-500">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
            <span>SGMC v2 — Concesión Transversal del Sisga S.A.S. (137 km)</span>
            <div className="flex items-center gap-3">
              <span className="inline-flex items-center gap-1 text-emerald-400">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                PostGIS & PWA Offline Activo
              </span>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
