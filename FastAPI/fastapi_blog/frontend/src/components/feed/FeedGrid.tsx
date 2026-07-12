"use client";
import Link from "next/link";
import type { Post, ListStatus } from "@/lib/types";
import FeedCard from "./FeedCard";
import FeedSkeleton from "./FeedSkeleton";
import Button from "@/components/ui/Button";
import { useAuth } from "@/store/auth";

type Props = {
  status: ListStatus;
  items: Post[];
  onRetry?: () => void;
  emptyTitle?: string;
  emptyCta?: React.ReactNode;
  topic?:string;
};

function StateBox({ tone, icon, title, action }: { tone: "tint" | "danger"; icon: string; title: string; action: React.ReactNode }) {
  return (
    <div className="py-20 flex flex-col items-center text-center gap-3">
      <div className={`w-12 h-12 grid place-items-center rounded-xl text-xl ${tone === "tint" ? "bg-tint text-accent" : "bg-danger-bg text-danger"}`}>{icon}</div>
      <p className="text-lg font-semibold text-ink">{title}</p>
      {action}
    </div>
  );
}

export default function FeedGrid({ status, items, onRetry, emptyTitle = "No posts yet", emptyCta, topic  }: Props) {
  const { currentUser } = useAuth();

  if (status === "loading" || status === "idle") return <FeedSkeleton />;
  if (status === "error") return <StateBox tone="danger" icon="!" title="Couldn't load posts" action={<Button variant="secondary" onClick={onRetry}>↻ Retry</Button>} />;
  if (status === "empty" || items.length === 0)
    return currentUser ? (
      <StateBox tone="tint" icon="✎" title={emptyTitle} action={emptyCta ?? <Link href="/posts/new"><Button>Write a post</Button></Link>} />
    ) : (
      <StateBox tone="tint" icon="" title="No posts for this section" action={<Link href="/login"><Button>Log in to write post</Button></Link>} />
    );

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-[22px]">
      {items.map((p) => <FeedCard key={p.id} post={p} />)}
    </div>
  );
}