"use client";
import { cn } from "@/lib/cn";

type Props = React.TextareaHTMLAttributes<HTMLTextAreaElement> & { label?: string; counter?: React.ReactNode; error?: string | null };

export default function Textarea({ label, counter, error, className, id, ...rest }: Props) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && <label htmlFor={id} className="text-[13px] font-medium text-text">{label}</label>}
      <textarea
        id={id}
        className={cn(
          "focus-ring min-h-[220px] p-3 rounded-[9px] bg-surface text-text text-sm border transition-colors placeholder:text-subtle resize-y",
          error ? "border-danger" : "border-border-strong",
          className
        )}
        {...rest}
      />
      {counter && <div className="font-mono text-xs text-subtle">{counter}</div>}
      {error && <p className="text-xs text-danger">{error}</p>}
    </div>
  );
}