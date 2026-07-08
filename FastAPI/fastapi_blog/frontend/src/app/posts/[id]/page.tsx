"use client";
import { use, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Tag from "@/components/ui/Tag";
import Avatar from "@/components/ui/Avatar";
import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";
import { useAuth } from "@/store/auth";
import { useToast } from "@/store/toast";

export default function PostDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { isOwner } = useAuth();
  const push = useToast((s) => s.push);
  const router = useRouter();
  const [confirm, setConfirm] = useState(false);

  // TODO: fetch post by id; placeholder below
  const post = {
    id, title: "Designing a content-first reading experience",
    topic: "Design", authorId: "me", author: { username: "Aniket", handle: "aniket", avatarUrl: undefined },
    createdAt: new Date().toISOString(), readTime: 5,
    content: "Long-form body goes here…",
  };

  const del = () => { setConfirm(false); push("Post deleted"); router.push("/"); };

  return (
    <article className="max-w-[680px] mx-auto py-4">
      <Tag>{post.topic}</Tag>
      <h1 className="mt-3 font-serif text-[40px] leading-tight font-bold text-ink">{post.title}</h1>

      <div className="mt-5 flex items-center justify-between">
        <Link href={`/u/${post.author.handle}`} className="flex items-center gap-3">
          <Avatar src={post.author.avatarUrl} size={46} />
          <div>
            <p className="text-sm font-semibold text-text">{post.author.username}</p>
            <p className="text-xs text-faint">{new Date(post.createdAt).toLocaleDateString()} · {post.readTime} min read</p>
          </div>
        </Link>
        {isOwner(post.authorId) && (
          <div className="flex gap-2">
            <Link href={`/posts/${id}/edit`}><Button variant="secondary">✎ Edit</Button></Link>
            <Button variant="danger" onClick={() => setConfirm(true)}>🗑 Delete</Button>
          </div>
        )}
      </div>

      <div className="mt-8 font-serif text-[18px] leading-[1.75] text-text space-y-5">
        <p>{post.content}</p>
        <blockquote className="border-l-[3px] border-primary pl-4 italic text-accent">A quote renders like this.</blockquote>
      </div>

      <Modal
        open={confirm} onClose={() => setConfirm(false)} icon="🗑"
        title="Delete this post?" description={`"${post.title}" will be permanently removed.`}
        confirmLabel="Delete post" onConfirm={del}
      />
    </article>
  );
}