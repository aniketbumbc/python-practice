import { create } from 'zustand';
import type { User } from '@/lib/types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:8000/api';

type ApiUser = {
  id: number;
  username: string;
  email: string;
  image_file: string | null;
  image_path: string;
};

const validImage = (url: string | null | undefined) =>
  url && url !== 'Image not found' ? url : undefined;

function toUser(u: ApiUser): User {
  return {
    id: String(u.id),
    username: u.username,
    handle: u.username,
    email: u.email,
    avatarUrl: validImage(u.image_path),
    postCount: 0,
  };
}

async function apiErrorMessage(res: Response, fallback: string) {
  const body = await res.json().catch(() => null);
  if (typeof body?.detail === 'string') return body.detail;
  if (res.status === 422) return 'Please check your details and try again.';
  return fallback;
}

type RegisterInput = { username: string; email: string; password: string };
type ProfileInput = { username: string; email: string };
type PasswordInput = { current_password: string; new_password: string };

type AuthState = {
  currentUser: User | null;
  token: string | null;
  registerStatus: 'idle' | 'loading' | 'error';
  registerError: string | null;
  login: (u: User, token?: string) => void;
  logout: () => void;
  isOwner: (authorId: string) => boolean;
  register: (input: RegisterInput) => Promise<boolean>;
  signIn: (username: string, password: string) => Promise<{ ok: true } | { ok: false; error: string }>;
  updateProfile: (input: ProfileInput) => Promise<{ ok: true } | { ok: false; error: string }>;
  changePassword: (input: PasswordInput) => Promise<{ ok: true } | { ok: false; error: string }>;
  deleteAccount: () => Promise<{ ok: true } | { ok: false; error: string }>;
  uploadAvatar: (file: File, onProgress: (pct: number) => void) => Promise<{ ok: true } | { ok: false; error: string }>;
  removeAvatar: () => Promise<{ ok: true } | { ok: false; error: string }>;
};

export const useAuth = create<AuthState>((set, get) => ({
  currentUser: null,
  token: null,
  registerStatus: 'idle',
  registerError: null,
  login: (u, token) => set({ currentUser: u, token: token ?? get().token }),
  logout: () => set({ currentUser: null, token: null }),
  isOwner: (authorId) => get().currentUser?.id === authorId,

  register: async (input) => {
    set({ registerStatus: 'loading', registerError: null });
    try {
      const res = await fetch(`${API_BASE}/users/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      });

      if (!res.ok) {
        const message = await apiErrorMessage(res, 'Registration failed');
        set({ registerStatus: 'error', registerError: message });
        return false;
      }

      const data: ApiUser = await res.json();
      set({ currentUser: toUser(data), registerStatus: 'idle', registerError: null });
      return true;
    } catch {
      set({ registerStatus: 'error', registerError: 'Registration failed. Please try again.' });
      return false;
    }
  },

  signIn: async (username, password) => {
    try {
      const form = new URLSearchParams();
      form.append('username', username);
      form.append('password', password);

      const tokenRes = await fetch(`${API_BASE}/users/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: form,
      });
      if (!tokenRes.ok) {
        const message = tokenRes.status === 401
          ? 'Incorrect username or password.'
          : await apiErrorMessage(tokenRes, 'Login failed');
        return { ok: false, error: message };
      }
      const { access_token }: { access_token: string; token_type: string } = await tokenRes.json();

      const meRes = await fetch(`${API_BASE}/users/me`, {
        headers: { Authorization: `Bearer ${access_token}` },
      });
      if (!meRes.ok) return { ok: false, error: 'Login failed. Please try again.' };
      const me: ApiUser = await meRes.json();

      set({ currentUser: toUser(me), token: access_token });
      return { ok: true };
    } catch {
      return { ok: false, error: 'Login failed. Please try again.' };
    }
  },

  updateProfile: async (input) => {
    const { currentUser, token } = get();
    if (!currentUser) return { ok: false, error: 'Not signed in.' };
    try {
      const res = await fetch(`${API_BASE}/users/${currentUser.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(input),
      });
      if (!res.ok) return { ok: false, error: await apiErrorMessage(res, 'Could not update profile') };
      const data: ApiUser = await res.json();
      set({ currentUser: toUser(data) });
      return { ok: true };
    } catch {
      return { ok: false, error: 'Could not update profile. Please try again.' };
    }
  },

  changePassword: async (input) => {
    const { token } = get();
    try {
      const res = await fetch(`${API_BASE}/users/me/password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(input),
      });
      if (!res.ok) return { ok: false, error: await apiErrorMessage(res, 'Could not update password') };
      return { ok: true };
    } catch {
      return { ok: false, error: 'Could not update password. Please try again.' };
    }
  },

  deleteAccount: async () => {
    const { currentUser, token } = get();
    if (!currentUser) return { ok: false, error: 'Not signed in.' };
    try {
      const res = await fetch(`${API_BASE}/users/${currentUser.id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) return { ok: false, error: await apiErrorMessage(res, 'Could not delete account') };
      set({ currentUser: null, token: null });
      return { ok: true };
    } catch {
      return { ok: false, error: 'Could not delete account. Please try again.' };
    }
  },

  uploadAvatar: (file, onProgress) => {
    const { currentUser, token } = get();
    if (!currentUser) return Promise.resolve({ ok: false, error: 'Not signed in.' });

    return new Promise((resolve) => {
      const form = new FormData();
      form.append('file', file);

      const xhr = new XMLHttpRequest();
      xhr.open('PATCH', `${API_BASE}/users/${currentUser.id}/picture`);
      xhr.setRequestHeader('Authorization', `Bearer ${token}`);

      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) onProgress(Math.round((e.loaded / e.total) * 100));
      };

      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          const data: ApiUser = JSON.parse(xhr.responseText);
          set({ currentUser: toUser(data) });
          resolve({ ok: true });
        } else {
          const detail = (() => {
            try { return JSON.parse(xhr.responseText)?.detail; } catch { return null; }
          })();
          resolve({ ok: false, error: typeof detail === 'string' ? detail : 'Could not upload image' });
        }
      };
      xhr.onerror = () => resolve({ ok: false, error: 'Could not upload image. Please try again.' });

      xhr.send(form);
    });
  },

  removeAvatar: async () => {
    const { currentUser, token } = get();
    if (!currentUser) return { ok: false, error: 'Not signed in.' };
    try {
      const res = await fetch(`${API_BASE}/users/${currentUser.id}/picture`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) return { ok: false, error: await apiErrorMessage(res, 'Could not remove image') };
      const data: ApiUser = await res.json();
      set({ currentUser: toUser(data) });
      return { ok: true };
    } catch {
      return { ok: false, error: 'Could not remove image. Please try again.' };
    }
  },
}));
