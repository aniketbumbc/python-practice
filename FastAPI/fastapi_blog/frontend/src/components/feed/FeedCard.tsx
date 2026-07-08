import Link from "next/link";
import Card from "@/components/ui/Card";
import Tag from "@/components/ui/Tag";
import Avatar from "@/components/ui/Avatar";
import type { Post } from "@/lib/types";

export default function FeedCard({ post }: { post: Post }) {
  return (
    <Link href={`/posts/${post.id}`}>
      <Card className="overflow-hidden rounded-[14px] hover:-translate-y-0.5 transition-transform">
        <div className="h-[140px] placeholder-stripes" style={post.coverUrl ? { backgroundImage: `url(${post.coverUrl})`, backgroundSize: "cover" } : undefined} />
        <div className="p-4">
          <Tag>{post.topic}</Tag>
          <h3 className="mt-2 font-serif text-xl font-semibold text-ink leading-snug">{post.title}</h3>
          <p className="mt-1.5 text-sm text-muted line-clamp-2">{post.excerpt}</p>
          <div className="mt-3 flex items-center gap-2">
            <Avatar src={post.author.avatarUrl} size={26} />
            <span className="text-sm text-text">{post.author.username}</span>
            <span className="text-xs text-faint">· {new Date(post.createdAt).toLocaleDateString()}</span>
          </div>
        </div>
      </Card>
    </Link>
  );
}