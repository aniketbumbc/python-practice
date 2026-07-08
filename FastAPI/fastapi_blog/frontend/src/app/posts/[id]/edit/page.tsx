import PostEditor from "@/components/post/PostEditor";
// TODO: fetch initial post by params.id and pass as `initial`
export default function EditPostPage() {
  return <PostEditor mode="edit" initial={{ title: "", topic: "", content: "" }} />;
}