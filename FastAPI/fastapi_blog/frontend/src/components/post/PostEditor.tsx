"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Input from "@/components/ui/Input";
import Textarea from "@/components/ui/Textarea";
import Button from "@/components/ui/Button";
import Tag from "@/components/ui/Tag";
import { useToast } from "@/store/toast";

type Props = { mode: "create" | "edit"; initial?: { title: string; topic: string; content: string } };

export default function PostEditor({ mode, initial }: Props) {
  const [title, setTitle] = useState(initial?.title ?? "");
  const [topic, setTopic] = useState(initial?.topic ?? "");
  const [content, setContent] = useState(initial?.content ?? "");
  const push = useToast((s) => s.push);
  const router = useRouter();

  const contentOk = content.length >= 30;
  const canPublish = title && topic.length >= 5 && contentOk;

  const publish = () => {
    if (!canPublish) return;
    push(mode === "create" ? "Published" : "Post updated");
    router.push("/");
  };

  return (
    <div className="max-w-[720px] mx-auto py-4">
      <div className="flex items-center justify-between mb-6">
        <Button variant="ghost" onClick={() => router.back()}>Cancel</Button>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => push("Draft saved")}>Save draft</Button>
          <Button onClick={publish} disabled={!canPublish}>{mode === "create" ? "Publish" : "Save changes"}</Button>
        </div>
      </div>

      <div className="space-y-5">
        <Input label="Title" value={title} maxLength={100} onChange={(e) => setTitle(e.target.value)}
          hint={`${title.length} / 100`} />
        <div>
          <Input label="Topic" value={topic} onChange={(e) => setTopic(e.target.value)} hint="At least 5 characters" />
          {topic.length >= 5 && <div className="mt-2"><Tag>{topic}</Tag></div>}
        </div>
        <Textarea label="Content" value={content} onChange={(e) => setContent(e.target.value)}
          counter={<span className={contentOk ? "text-success" : undefined}>{content.length} chars · min 30 {contentOk && "✓"}</span>} />
      </div>
    </div>
  );
}