// TODO: validation rules mirroring backend
export const rules = {
  password: (v: string) =>
    v.length >= 5 || 'Password must be at least 5 characters.',
  content: (v: string) =>
    v.length >= 30 || 'Content must be at least 30 characters.',
  topic: (v: string) => v.length >= 5 || 'Topic must be at least 5 characters.',
  username: (v: string) =>
    (v.length >= 1 && v.length <= 50) || 'Username must be 1–50 characters.',
  email: (v: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Enter a valid email.',
};

export type Rule = (v: string) => true | string;
export const check = (v: string, r: Rule) => {
  const res = r(v);
  return res === true ? null : res;
};
