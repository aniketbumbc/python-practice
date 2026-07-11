"use client";
import { use, useEffect } from "react";
import PostEditor from "@/components/post/PostEditor";
import Button from "@/components/ui/Button";
import { useBlogStore } from "@/store/blog";

export default function EditPostPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { currentPost: post, postStatus, postError, fetchPost } = useBlogStore();

  useEffect(() => {
    fetchPost(id);
  }, [id, fetchPost]);

  if (postStatus === "loading" || postStatus === "idle") {
    return (
      <div className="max-w-[720px] mx-auto py-4 space-y-4 animate-pulse">
        <div className="h-10 w-full bg-divider rounded" />
        <div className="h-10 w-1/2 bg-divider rounded" />
        <div className="h-40 w-full bg-divider rounded" />
      </div>
    );
  }

  if (postStatus === "error" || !post) {
    return (
      <div className="max-w-[720px] mx-auto py-20 flex flex-col items-center text-center gap-3">
        <div className="w-12 h-12 grid place-items-center rounded-xl text-xl bg-danger-bg text-danger">!</div>
        <p className="text-lg font-semibold text-ink">{postError ?? "Couldn't load post"}</p>
        <Button variant="secondary" onClick={() => fetchPost(id)}>↻ Retry</Button>
      </div>
    );
  }

  return (
    <PostEditor
      mode="edit"
      postId={id}
      initial={{ title: post.title, topic: post.topic, content: post.content, coverUrl: post.coverUrl }}
    />
  );
}