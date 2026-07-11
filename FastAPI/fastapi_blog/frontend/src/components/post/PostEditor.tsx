"use client";
import { useRef, useState } from "react";
import { useRouter } from "next/navigation";
import Input from "@/components/ui/Input";
import Textarea from "@/components/ui/Textarea";
import Button from "@/components/ui/Button";
import Tag from "@/components/ui/Tag";
import { useToast } from "@/store/toast";
import { useAuth } from "@/store/auth";
import { useBlogStore } from "@/store/blog";

type Props = {
  mode: "create" | "edit";
  postId?: string;
  initial?: { title: string; topic: string; content: string; coverUrl?: string };
};

export default function PostEditor({ mode, postId, initial }: Props) {
  const [title, setTitle] = useState(initial?.title ?? "");
  const [topic, setTopic] = useState(initial?.topic ?? "");
  const [content, setContent] = useState(initial?.content ?? "");
  const [publishing, setPublishing] = useState(false);
  const [preview, setPreview] = useState<string | null>(initial?.coverUrl ?? null);
  const [pendingFile, setPendingFile] = useState<File | null>(null);
  const [uploadPct, setUploadPct] = useState<number | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const push = useToast((s) => s.push);
  const token = useAuth((s) => s.token);
  const createPost = useBlogStore((s) => s.createPost);
  const updatePost = useBlogStore((s) => s.updatePost);
  const uploadThumbnail = useBlogStore((s) => s.uploadThumbnail);
  const router = useRouter();

  const contentOk = content.length >= 30;
  const contentErr = content && !contentOk ? "Content must be at least 30 characters." : null;
  const topicOk = topic.length > 1;
  const topicErr = topic && !topicOk ? "Topic must be more than 1 character." : null;
  const canPublish = title && topicOk && contentOk;

  const onFileSelected = async (file: File) => {
    if (!file.type.startsWith("image/")) {
      push("Only image files are supported.", "error");
      return;
    }
    setPreview(URL.createObjectURL(file));

    if (mode === "edit" && postId) {
      setUploadPct(0);
      const result = await uploadThumbnail(postId, file, token, setUploadPct);
      setUploadPct(null);
      if (!result.ok) {
        push(result.error, "error");
        return;
      }
      push("Thumbnail updated");
    } else {
      setPendingFile(file);
    }
  };

  const publish = async () => {
    if (!canPublish || publishing) return;
    setPublishing(true);
    const input = { title, topic, content };
    const result = mode === "create" ? await createPost(input, token) : await updatePost(postId!, input, token);

    if (!result.ok) {
      setPublishing(false);
      push(result.error, "error");
      return;
    }

    if (mode === "create" && pendingFile) {
      await uploadThumbnail(result.post.id, pendingFile, token, () => {});
    }

    setPublishing(false);
    push(mode === "create" ? "Published" : "Post updated");
    router.push(`/posts/${result.post.id}`);
  };

  return (
    <div className="max-w-[720px] mx-auto py-4">
      <div className="flex items-center justify-between mb-6">
        <Button variant="ghost" onClick={() => router.back()}>Cancel</Button>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => fileInputRef.current?.click()} disabled={uploadPct !== null}>
            {uploadPct !== null ? `Uploading… ${uploadPct}%` : "⬆ Upload image"}
          </Button>
          <Button variant="secondary" onClick={() => push("Draft saved")}>Save draft</Button>
          <Button onClick={publish} disabled={!canPublish || publishing}>
            {publishing ? "Saving…" : mode === "create" ? "Publish" : "Save changes"}
          </Button>
        </div>
      </div>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) onFileSelected(file);
          e.target.value = "";
        }}
      />

      <div className="space-y-5">
        <div
          className="h-64 rounded-2xl overflow-hidden placeholder-stripes cursor-pointer"
          style={preview ? { backgroundImage: `url(${preview})`, backgroundSize: "cover", backgroundPosition: "center" } : undefined}
          onClick={() => fileInputRef.current?.click()}
        />
        <Input label="Title" value={title} maxLength={100} onChange={(e) => setTitle(e.target.value)}
          hint={`${title.length} / 100`} />
        <div>
          <Input label="Topic" value={topic} onChange={(e) => setTopic(e.target.value)} error={topicErr} hint="More than 1 character" />
          {topic.length >= 5 && <div className="mt-2"><Tag>{topic}</Tag></div>}
        </div>
        <Textarea label="Content" value={content} onChange={(e) => setContent(e.target.value)}
          error={contentErr}
          counter={<span className={contentOk ? "text-success" : undefined}>{content.length} chars · min 30 {contentOk && "✓"}</span>} />
      </div>
    </div>
  );
}