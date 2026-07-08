"use client";
import { cn } from "@/lib/cn";

type Variant = "primary" | "secondary" | "ghost" | "danger";
type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant };

const base = "focus-ring cursor-pointer inline-flex items-center justify-center gap-2 h-[42px] px-4 rounded-[9px] text-sm font-semibold transition-colors disabled:opacity-45 disabled:cursor-not-allowed";

const variants: Record<Variant, string> = {
  primary:   "bg-primary text-ink hover:bg-primary-hover",
  secondary: "bg-surface text-text border border-border-strong hover:border-muted",
  ghost:     "text-text hover:bg-surface",
  danger:    "bg-danger text-white hover:opacity-90",
};

export default function Button({ variant = "primary", className, ...rest }: Props) {
  return <button className={cn(base, variants[variant], className)} {...rest} />;
}