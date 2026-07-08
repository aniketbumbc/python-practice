"use client";
import { useEffect } from "react";
import Button from "./Button";

type Props = {
  open: boolean;
  onClose: () => void;
  icon?: React.ReactNode;
  title: string;
  description?: string;
  confirmLabel: string;
  onConfirm: () => void;
  confirmDisabled?: boolean;
  children?: React.ReactNode; // e.g. the "type username" input
};

export default function Modal({ open, onClose, icon, title, description, confirmLabel, onConfirm, confirmDisabled, children }: Props) {
  useEffect(() => {
    const onEsc = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    if (open) document.addEventListener("keydown", onEsc);
    return () => document.removeEventListener("keydown", onEsc);
  }, [open, onClose]);

  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 grid place-items-center p-4" style={{ background: "rgba(16,21,31,.42)" }} onClick={onClose}>
      <div className="w-full max-w-[420px] bg-surface rounded-[16px] shadow-[var(--shadow-modal)] p-6" onClick={(e) => e.stopPropagation()}>
        {icon && <div className="mb-3 w-11 h-11 grid place-items-center rounded-xl bg-danger-bg text-danger text-lg">{icon}</div>}
        <h2 className="font-serif text-xl font-semibold text-ink">{title}</h2>
        {description && <p className="mt-1.5 text-sm text-muted">{description}</p>}
        {children && <div className="mt-4">{children}</div>}
        <div className="mt-6 flex justify-end gap-2">
          <Button variant="secondary" onClick={onClose}>Cancel</Button>
          <Button variant="danger" onClick={onConfirm} disabled={confirmDisabled}>{confirmLabel}</Button>
        </div>
      </div>
    </div>
  );
}