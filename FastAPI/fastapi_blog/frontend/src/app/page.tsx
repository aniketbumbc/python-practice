"use client";
import { useEffect, useState } from "react";
import FeedGrid from "@/components/feed/FeedGrid";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/cn";
import { useBlogStore } from "@/store/blog";

const TOPICS = ["All", "Engineering", "Design", "Product", "AI"];

export default function HomePage() {
  const { posts, status, hasMore, fetchPosts, loadMore } = useBlogStore();
  const [topic, setTopic] = useState("All");

  useEffect(() => {
    fetchPosts({ skip: 0, limit: 10 });
  }, [fetchPosts]);

  const visibleItems = topic === "All" ? posts : posts.filter((p) => p.topic === topic);

  return (
    <>
      <div className="flex items-start justify-between gap-4 mb-6">
        <div>
          <h1 className="font-serif text-[32px] font-bold text-ink">Latest posts</h1>
          <p className="text-muted mt-1">Fresh writing from the community.</p>
        </div>
        <div className="flex flex-wrap gap-2 justify-end">
          {TOPICS.map((t) => (
            <button
              key={t}
              onClick={() => setTopic(t)}
              className={cn("focus-ring cursor-pointer px-3 py-1.5 rounded-full text-sm border transition-colors",
                topic === t ? "bg-primary text-ink border-primary" : "bg-surface text-text border-border-strong hover:border-muted")}
            >{t}</button>
          ))}
        </div>
      </div>

      <FeedGrid status={status} items={visibleItems} onRetry={() => fetchPosts({ skip: 0, limit: 10 })} />

      {status === "success" && hasMore && (
        <div className="mt-8 flex justify-center">
          <Button variant="secondary" onClick={loadMore}>Load more</Button>
        </div>
      )}
    </>
  );
}