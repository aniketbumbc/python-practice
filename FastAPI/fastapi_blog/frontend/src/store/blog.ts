import { create } from 'zustand';
import type { Post, ListStatus } from '@/lib/types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:8000/api';

type ApiUser = {
  id: number;
  username: string;
  image_file: string | null;
  image_path: string;
};

type ApiPost = {
  id: number;
  user_id: number;
  title: string;
  content: string;
  topic: string;
  date_posted: string;
  author: ApiUser;
  blog_image_file: string | null;
  blog_image_path: string;
};

type PaginatedPostResponse = {
  posts: ApiPost[];
  total: number;
  skip: number;
  limit: number;
  has_more: boolean;
};

const validImage = (url: string | null | undefined) =>
  url && url !== 'Image not found' ? url : undefined;

const excerptOf = (content: string, len = 160) =>
  content.length > len ? `${content.slice(0, len).trim()}…` : content;

const readTimeOf = (content: string) =>
  Math.max(1, Math.round(content.split(/\s+/).length / 200));

function toPost(p: ApiPost): Post {
  return {
    id: String(p.id),
    title: p.title,
    topic: p.topic,
    excerpt: excerptOf(p.content),
    content: p.content,
    coverUrl: validImage(p.blog_image_path),
    author: {
      id: String(p.author.id),
      username: p.author.username,
      handle: p.author.username,
      avatarUrl: validImage(p.author.image_path),
    },
    createdAt: p.date_posted,
    readTime: readTimeOf(p.content),
  };
}

type BlogState = {
  posts: Post[];
  status: ListStatus;
  error: string | null;
  skip: number;
  limit: number;
  total: number;
  hasMore: boolean;
  currentPost: Post | null;
  postStatus: ListStatus;
  postError: string | null;
  fetchPosts: (opts?: { skip?: number; limit?: number; append?: boolean }) => Promise<void>;
  loadMore: () => Promise<void>;
  fetchPost: (id: string) => Promise<void>;
};

export const useBlogStore = create<BlogState>((set, get) => ({
  posts: [],
  status: 'idle',
  error: null,
  skip: 0,
  limit: 10,
  total: 0,
  hasMore: false,
  currentPost: null,
  postStatus: 'idle',
  postError: null,

  fetchPosts: async ({ skip = 0, limit = get().limit, append = false } = {}) => {
    set({ status: 'loading', error: null });
    try {
      const res = await fetch(`${API_BASE}/posts/?skip=${skip}&limit=${limit}`);
      if (!res.ok) throw new Error(`Request failed with status ${res.status}`);
      const data: PaginatedPostResponse = await res.json();
      const mapped = data.posts.map(toPost);

      set((s) => {
        const posts = append ? [...s.posts, ...mapped] : mapped;
        return {
          posts,
          status: posts.length ? 'success' : 'empty',
          skip: data.skip,
          limit: data.limit,
          total: data.total,
          hasMore: data.has_more,
        };
      });
    } catch (err) {
      set({
        status: 'error',
        error: err instanceof Error ? err.message : 'Failed to load posts',
      });
    }
  },

  loadMore: () => {
    const { skip, limit, hasMore, status } = get();
    if (!hasMore || status === 'loading') return Promise.resolve();
    return get().fetchPosts({ skip: skip + limit, limit, append: true });
  },

  fetchPost: async (id: string) => {
    set({ postStatus: 'loading', postError: null });
    try {
      const res = await fetch(`${API_BASE}/posts/${id}`);
      if (!res.ok) throw new Error(`Request failed with status ${res.status}`);
      const data: ApiPost = await res.json();
      set({ currentPost: toPost(data), postStatus: 'success' });
    } catch (err) {
      set({
        postStatus: 'error',
        postError: err instanceof Error ? err.message : 'Failed to load post',
      });
    }
  },
}));
