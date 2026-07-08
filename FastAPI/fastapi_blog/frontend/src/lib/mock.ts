import type { Post, User } from '@/lib/types';

export const mockUsers: User[] = [
  {
    id: 'u1',
    username: 'Aniket Bhavsar',
    handle: 'aniket',
    email: 'aniket@blog.dev',
    postCount: 4,
  },
  {
    id: 'u2',
    username: 'Mira Sethi',
    handle: 'mira',
    email: 'mira@blog.dev',
    postCount: 2,
  },
  {
    id: 'u3',
    username: 'Dev Rao',
    handle: 'devrao',
    email: 'dev@blog.dev',
    postCount: 3,
  },
  {
    id: 'u4',
    username: 'Lena Ortiz',
    handle: 'lena',
    email: 'lena@blog.dev',
    postCount: 1,
  },
  {
    id: 'u5',
    username: 'Kojo Mensah',
    handle: 'kojo',
    email: 'kojo@blog.dev',
    postCount: 5,
  },
  {
    id: 'u6',
    username: 'Sara Kim',
    handle: 'sara',
    email: 'sara@blog.dev',
    postCount: 2,
  },
];

const author = (u: User): Post['author'] => ({
  id: u.id,
  username: u.username,
  handle: u.handle,
  avatarUrl: u.avatarUrl,
});

export const mockPosts: Post[] = [
  {
    id: 'p1',
    title: 'Designing a content-first reading experience',
    topic: 'Design',
    excerpt:
      'Why the reading column, not the chrome, should drive every layout decision on a publishing platform.',
    content:
      'The reading column is the product. Everything else is scaffolding around the words. When you start there, spacing, type scale, and line length stop being guesswork and become derived constraints.\n\nWe set the body at 18px with a 1.75 line-height and never let the measure exceed ~680px. Anything wider and the eye loses its place on the return sweep.',
    author: author(mockUsers[0]),
    createdAt: '2026-06-28T10:00:00Z',
    readTime: 5,
  },
  {
    id: 'p2',
    title: 'Shipping a FastAPI backend that scales',
    topic: 'Engineering',
    excerpt:
      "Async SQLAlchemy, connection pooling, and the mistakes I made so you don't have to.",
    content:
      "Async everywhere sounds great until your connection pool quietly saturates under load. Here's how we tuned pool_size and max_overflow against real traffic.",
    author: author(mockUsers[2]),
    createdAt: '2026-06-25T09:30:00Z',
    readTime: 8,
  },
  {
    id: 'p3',
    title: 'Tokenization, embeddings, and why they matter',
    topic: 'AI',
    excerpt:
      'A ground-up explainer on how text becomes vectors, without the hand-waving.',
    content:
      'Before a model reasons about anything, it chops your text into tokens and maps them to vectors. Get this mental model right and the rest of the stack stops feeling like magic.',
    author: author(mockUsers[1]),
    createdAt: '2026-06-22T14:15:00Z',
    readTime: 6,
  },
  {
    id: 'p4',
    title: 'The case for boring product decisions',
    topic: 'Product',
    excerpt:
      'Novelty is a tax. Most of the time your users want the obvious thing done well.',
    content:
      'Every clever interaction you invent is something your users have to learn. Boring, predictable patterns are a feature, not a failure of imagination.',
    author: author(mockUsers[4]),
    createdAt: '2026-06-20T08:00:00Z',
    readTime: 4,
  },
  {
    id: 'p5',
    title: 'State management without the ceremony',
    topic: 'Engineering',
    excerpt:
      'How Zustand replaced 300 lines of context boilerplate in an afternoon.',
    content:
      "Context is fine until it isn't. When re-renders start cascading, a small external store like Zustand gives you surgical subscriptions with almost no API surface.",
    author: author(mockUsers[0]),
    createdAt: '2026-06-18T11:45:00Z',
    readTime: 5,
  },
  {
    id: 'p6',
    title: 'Type scales that actually breathe',
    topic: 'Design',
    excerpt:
      'Picking a modular scale and sticking to it is 80% of good typography.',
    content:
      'A consistent ratio between sizes does more for perceived polish than any font choice. Lock the scale, then only ever reach for steps that exist on it.',
    author: author(mockUsers[5]),
    createdAt: '2026-06-15T16:20:00Z',
    readTime: 3,
  },
];

// simulate async so loading/empty/error states still render
export function fetchPosts({
  empty = false,
  fail = false,
  delay = 700,
} = {}): Promise<Post[]> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (fail) return reject(new Error('mock failure'));
      resolve(empty ? [] : mockPosts);
    }, delay);
  });
}

export const findUser = (handle: string) =>
  mockUsers.find((u) => u.handle === handle) ?? null;
export const findPost = (id: string) =>
  mockPosts.find((p) => p.id === id) ?? null;
export const postsByAuthor = (userId: string) =>
  mockPosts.filter((p) => p.author.id === userId);
