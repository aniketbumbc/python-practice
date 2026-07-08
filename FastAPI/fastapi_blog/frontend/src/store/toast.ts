import { create } from 'zustand';

export type Toast = { id: string; message: string; kind: 'success' | 'error' };

type ToastState = {
  toasts: Toast[];
  push: (message: string, kind?: Toast['kind']) => void;
  dismiss: (id: string) => void;
};

export const useToast = create<ToastState>((set) => ({
  toasts: [],
  push: (message, kind = 'success') => {
    const id = crypto.randomUUID();
    set((s) => ({ toasts: [...s.toasts, { id, message, kind }] }));
    setTimeout(
      () => set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),
      3200,
    );
  },
  dismiss: (id) =>
    set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),
}));
