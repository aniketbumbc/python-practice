"use client";
import { useToast } from "@/store/toast";

export default function ToastHost() {
  const { toasts } = useToast();
  return (
    <div className="fixed bottom-5 left-1/2 -translate-x-1/2 z-[60] flex flex-col gap-2 items-center">
      {toasts.map((t) => (
        <div key={t.id} className="flex items-center gap-2.5 px-4 py-2.5 rounded-[10px] text-sm text-white shadow-lg" style={{ background: "#10151F" }}>
          <span className="w-2 h-2 rounded-full" style={{ background: t.kind === "success" ? "#37C98A" : "#FF6B5B" }} />
          {t.message}
        </div>
      ))}
    </div>
  );
}