"use client";
import { use, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Tag from "@/components/ui/Tag";
import Avatar from "@/components/ui/Avatar";
import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";
import { useAuth } from "@/store/auth";
import { useToast } from "@/store/toast";
import { useBlogStore } from "@/store/blog";

export default function PostDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { isOwner, token } = useAuth();
  const push = useToast((s) => s.push);
  const router = useRouter();
  const [confirm, setConfirm] = useState(false);
  const [uploadPct, setUploadPct] = useState<number | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { currentPost: post, postStatus, postError, fetchPost, uploadThumbnail } = useBlogStore();

  useEffect(() => {
    fetchPost(id);
  }, [id, fetchPost]);

  const del = () => { setConfirm(false); push("Post deleted"); router.push("/"); };

  const uploadFile = async (file: File) => {
    if (!file.type.startsWith("image/")) {
      push("Only image files are supported.", "error");
      return;
    }
    setUploadPct(0);
    const result = await uploadThumbnail(id, file, token, setUploadPct);
    setUploadPct(null);
    if (!result.ok) {
      push(result.error, "error");
      return;
    }
    push("Thumbnail updated");
  };

  if (postStatus === "loading" || postStatus === "idle") {
    return (
      <div className="max-w-[680px] mx-auto py-4 space-y-4 animate-pulse">
        <div className="h-6 w-20 bg-divider rounded-full" />
        <div className="h-10 w-full bg-divider rounded" />
        <div className="h-6 w-2/3 bg-divider rounded" />
      </div>
    );
  }

  if (postStatus === "error" || !post) {
    return (
      <div className="max-w-[680px] mx-auto py-20 flex flex-col items-center text-center gap-3">
        <div className="w-12 h-12 grid place-items-center rounded-xl text-xl bg-danger-bg text-danger">!</div>
        <p className="text-lg font-semibold text-ink">{postError ?? "Couldn't load post"}</p>
        <Button variant="secondary" onClick={() => fetchPost(id)}>↻ Retry</Button>
      </div>
    );
  }

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
        {isOwner(post.author.id) && (
          <div className="flex gap-2">
            <Link href={`/posts/${id}/edit`}><Button variant="secondary">✎ Edit</Button></Link>
            <Button variant="secondary" onClick={() => fileInputRef.current?.click()} disabled={uploadPct !== null}>
              {uploadPct !== null ? `Uploading… ${uploadPct}%` : "⬆ Upload"}
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) uploadFile(file);
                e.target.value = "";
              }}
            />
            <Button variant="danger" onClick={() => setConfirm(true)}>🗑 Delete</Button>
          </div>
        )}
      </div>

      <div
        className="mt-6 h-80 rounded-2xl overflow-hidden placeholder-stripes"
        style={post.coverUrl ? { backgroundImage: `url(${post.coverUrl})`, backgroundSize: "cover", backgroundPosition: "center" } : undefined}
      />

      <div className="mt-8 font-serif text-[18px] leading-[1.75] text-text space-y-5">
        <p>{post.content}</p>
      </div>

      <Modal
        open={confirm} onClose={() => setConfirm(false)} icon="🗑"
        title="Delete this post?" description={`"${post.title}" will be permanently removed.`}
        confirmLabel="Delete post" onConfirm={del}
      />
    </article>
  );
}