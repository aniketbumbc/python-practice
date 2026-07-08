export type User = {
  id: string;
  username: string;
  handle: string;
  email: string;
  avatarUrl?: string;
  postCount: number;
};

export type Post = {
  id: string;
  title: string;
  topic: string;
  excerpt: string;
  content: string;
  coverUrl?: string;
  author: Pick<User, 'id' | 'username' | 'handle' | 'avatarUrl'>;
  createdAt: string; // ISO
  readTime: number; // minutes
};

export type ListStatus = 'idle' | 'loading' | 'success' | 'empty' | 'error';
