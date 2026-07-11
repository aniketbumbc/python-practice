"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";
import AvatarUploader from "@/components/settings/AvatarUploader";
import { useAuth } from "@/store/auth";
import { useToast } from "@/store/toast";
import { rules, check } from "@/lib/validation";

export default function SettingsPage() {
  const { currentUser, updateProfile, changePassword, deleteAccount, uploadAvatar, removeAvatar, logout } = useAuth();
  const push = useToast((s) => s.push);
  const router = useRouter();

  const [username, setUsername] = useState(currentUser?.username ?? "");
  const [email, setEmail] = useState(currentUser?.email ?? "");
  const [profileError, setProfileError] = useState<string | null>(null);
  const [profileSaving, setProfileSaving] = useState(false);

  const [currentPw, setCurrentPw] = useState("");
  const [newPw, setNewPw] = useState("");
  const [confirmPw, setConfirmPw] = useState("");
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [passwordSaving, setPasswordSaving] = useState(false);

  const [confirmDelete, setConfirmDelete] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (currentUser) {
      setUsername(currentUser.username);
      setEmail(currentUser.email);
    }
  }, [currentUser]);

  if (!currentUser) {
    return (
      <div className="max-w-[420px] mx-auto py-20 text-center">
        <p className="text-lg font-semibold text-ink">You need to be signed in to view settings.</p>
        <Link href="/login" className="text-accent text-sm mt-2 inline-block">Log in</Link>
      </div>
    );
  }

  const usernameErr = username ? check(username, rules.username) : null;
  const emailErr = email ? check(email, rules.email) : null;
  const dirty = username !== currentUser.username || email !== currentUser.email;
  const profileValid = !usernameErr && !emailErr && username && email;

  const resetProfile = () => {
    setUsername(currentUser.username);
    setEmail(currentUser.email);
    setProfileError(null);
    router.push("/");
  };

  const saveProfile = async () => {
    if (!profileValid || !dirty) return;
    setProfileSaving(true);
    setProfileError(null);
    const result = await updateProfile({ username, email });
    setProfileSaving(false);
    if (result.ok) push("Profile updated");
    else setProfileError(result.error);
  };

  const newPwErr = newPw ? check(newPw, rules.password) : null;
  const mismatch = confirmPw && newPw !== confirmPw ? "Passwords don't match." : null;
  const passwordValid = currentPw && newPw && !newPwErr && !mismatch;

  const cancelPassword = () => {
    setCurrentPw("");
    setNewPw("");
    setConfirmPw("");
    setPasswordError(null);
    router.push("/");
  };

  const submitPassword = async () => {
    if (!passwordValid) return;
    setPasswordSaving(true);
    setPasswordError(null);
    const result = await changePassword({ current_password: currentPw, new_password: newPw });
    setPasswordSaving(false);
    if (result.ok) {
      push("Password updated");
      setCurrentPw(""); setNewPw(""); setConfirmPw("");
      logout();
      router.push("/");
    } else {
      setPasswordError(result.error);
    }
  };

  const confirmDeleteAccount = async () => {
    setDeleting(true);
    setDeleteError(null);
    const result = await deleteAccount();
    setDeleting(false);
    if (result.ok) {
      setConfirmDelete(false);
      logout();
      push("Account deleted");
      router.push("/");
    } else {
      setDeleteError(result.error);
    }
  };

  return (
    <div className="max-w-[720px] mx-auto py-4 space-y-6">
      <Card className="p-7">
        <h2 className="font-serif text-xl font-bold text-ink">Profile</h2>
        <p className="text-sm text-muted mt-1">This information appears on your public profile.</p>

        <div className="mt-5 grid grid-cols-1 sm:grid-cols-[220px_1fr] gap-6">
          <AvatarUploader
            src={currentUser.avatarUrl}
            onUpload={(file, onProgress) => uploadAvatar(file, onProgress)}
            onRemove={() => removeAvatar()}
          />
          <div className="space-y-4">
            <Input
              label="Username" value={username} onChange={(e) => setUsername(e.target.value)}
              error={usernameErr} valid={!!username && !usernameErr}
            />
            <Input
              label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)}
              error={emailErr ?? profileError} valid={!!email && !emailErr && !profileError}
            />
          </div>
        </div>

        <div className="mt-6 flex justify-end gap-2">
          <Button variant="secondary" onClick={resetProfile} disabled={profileSaving}>Cancel</Button>
          <Button onClick={saveProfile} disabled={!profileValid || !dirty || profileSaving}>
            {profileSaving ? "Saving…" : "Save profile"}
          </Button>
        </div>
      </Card>

      <Card className="p-7">
        <h2 className="font-serif text-xl font-bold text-ink">Change password</h2>

        <div className="mt-5 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Input
            label="Current" type="password" value={currentPw} onChange={(e) => setCurrentPw(e.target.value)}
            error={passwordError}
          />
          <Input label="New" type="password" value={newPw} onChange={(e) => setNewPw(e.target.value)} error={newPwErr} hint="At least 5 characters" />
          <Input label="Confirm new" type="password" value={confirmPw} onChange={(e) => setConfirmPw(e.target.value)} error={mismatch} />
        </div>

        <div className="mt-6 flex justify-end">
          <Button className="mr-2" variant="secondary" onClick={cancelPassword} disabled={passwordSaving}>Cancel</Button>
          <Button onClick={submitPassword} disabled={!passwordValid || passwordSaving}>
            {passwordSaving ? "Updating…" : "Update password"}
          </Button>
          
        </div>
      </Card>

      <Card className="p-7 border-danger-border">
        <h2 className="font-serif text-xl font-bold text-danger">Danger zone</h2>
        <div className="mt-4 flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-text">Delete account</p>
            <p className="text-sm text-muted">Permanently removes your account and all your posts.</p>
            {deleteError && <p className="mt-1 text-xs text-danger">{deleteError}</p>}
          </div>
          <Button variant="danger" onClick={() => setConfirmDelete(true)}>Delete account</Button>
        </div>
      </Card>

      <Modal
        open={confirmDelete} onClose={() => setConfirmDelete(false)} icon="🗑"
        title="Delete your account?"
        description="This permanently removes your account and all your posts. This can't be undone."
        confirmLabel={deleting ? "Deleting…" : "Delete account"}
        confirmDisabled={deleting}
        onConfirm={confirmDeleteAccount}
      />
    </div>
  );
}
