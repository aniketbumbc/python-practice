"use client";
import { cn } from "@/lib/cn";

type Props = React.InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  error?: string | null;
  valid?: boolean;
  hint?: string;
  labelRight?: React.ReactNode;
};

export default function Input({ label, error, valid, hint, labelRight, className, id, ...rest }: Props) {
  const inputId = id ?? rest.name;
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <div className="flex items-center justify-between">
          <label htmlFor={inputId} className="text-[13px] font-medium text-text">{label}</label>
          {labelRight}
        </div>
      )}
      <input
        id={inputId}
        className={cn(
          "focus-ring h-11 px-3 rounded-[9px] bg-surface text-text text-sm border transition-colors placeholder:text-subtle",
          error ? "border-danger" : valid ? "border-success" : "border-border-strong",
          className
        )}
        {...rest}
      />
      {error ? <p className="text-xs text-danger">{error}</p>
        : valid ? <p className="text-xs text-success">✓ Looks good</p>
        : hint ? <p className="text-xs text-subtle">{hint}</p> : null}
    </div>
  );
}