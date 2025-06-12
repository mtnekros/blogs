# Understanding Git LFS: Why You Need It for Large Files

When working with Git, everything seems smooth—until you start dealing with
large binary files like machine learning models, images, or videos. Git wasn’t
designed for that. This blog post explains **why Git struggles with large
files**, how **Git LFS (Large File Storage)** solves this, and how to set it
up.

---

## How Git Works (Simplified): Snapshots, Trees & Storage Efficiency

Git is a distributed version control system designed originally for tracking
source code. It stores the history of your project in a **Directed Acyclic
Graph (DAG)**.


### Commits Are Snapshots, Not Diffs

Git stores each commit as a **snapshot** of the entire project—not just
changes. Unlike diff-based systems, Git saves a full reference to the current
state of every file at that point in time.


### Git’s Object Model: Commit → Tree → Blobs
* **Commit object**
  * Contains metadata and points to:
    * A **tree object** (the root directory)
    * One or more **parent commits**
* **Tree object**
  * Represents a directory
  * Contains:
    * **Blobs** – raw file contents (not file names or paths)
    * **Other trees** – subdirectories
* **Blob object**
  * Stores file content
  * Identified by content hash (SHA-1/SHA-256)
* **Branches/Tags**
  * Simple pointers to specific commit objects

---

### Why It’s Still Efficient

Although each commit stores a snapshot, Git avoids redundancy through **content-addressed storage**:

> If a file hasn’t changed, Git reuses the same blob object in the new commit.
> Each unique version of a file is stored only once—no matter how many commits
> reference it.

This makes Git **memory-efficient for text/code**, since unchanged files don’t
consume extra space across commits.

* Git is fast for code, but not for large binary assets

### Solution: Use **Git LFS** to handle large binaries efficiently (covered separately)

---

Let me know if you want this formatted as a collapsible FAQ section or slide deck summary.

### Problem with Binary Files:

Let’s say you have a model file `model1.onnx` that is 500MB:

* You commit it 3 times after modifying it each time.
* Git stores 3 full snapshots → your repo now has **1500MB of history**.
* Every clone/pull/download of the repo pulls the entire history.
* Git becomes **slow and bloated**.

---

## 💡 What Is Git LFS?

**Git Large File Storage (LFS)** is an extension to Git that helps manage large files.

### What It Does:

* Replaces large files in your repository with **lightweight pointers**.
* Actual file contents are stored on a **remote Git LFS server** (like GitHub’s LFS server).
* GitHub, GitLab, Bitbucket, and others **support Git LFS**.

### Benefits:

* Git stays **fast and lightweight**.
* You only download the **specific version of a file** you need (based on your current commit).
* Git behaves as usual for everything else — you can still use `git commit`, `git push`, `git checkout`, etc.

---

## ⚙️ Setting Up Git LFS

Here’s how to start using Git LFS:

### 1. Install Git LFS

```bash
# macOS
brew install git-lfs

# Ubuntu
sudo apt install git-lfs

# Windows (via Chocolatey)
choco install git-lfs
```

Then run:

```bash
git lfs install
```

This sets up Git LFS for your user account.

---

### 2. Track Specific File Types

You tell Git which file types to manage with LFS:

```bash
git lfs track "*.onnx"
git lfs track "*.jpg"
```

This creates or updates a `.gitattributes` file in your repo.

---

### 3. Add, Commit, and Push as Usual

```bash
git add model1.onnx
git commit -m "Add large model"
git push
```

* Git replaces `model1.onnx` with a pointer in the repo.
* The actual file goes to the LFS server.

---

## 🔁 Switching Versions

When you `checkout` a previous commit:

* Git LFS **swaps in the correct version** of the large file.
* You don’t need to manually manage versions of your binary assets.

---

## 🧭 What Is a DAG?

Since Git's internal structure is a **Directed Acyclic Graph (DAG)**, here's a quick primer:

* **Directed**: Edges (arrows) point from older to newer commits.
* **Acyclic**: No loops — you can't return to the same node by following edges.
* Useful for:

  * Version history
  * Dependency resolution
  * Build pipelines

---

## ⚠️ Caveats of Git LFS

* Git LFS has **bandwidth and storage limits** on free GitHub plans:

  * 1 GB storage
  * 1 GB/month bandwidth
* You may need to **purchase additional data packs** for large projects.
* Tools like `git archive` and some CI systems may not support LFS out of the box.

---

## ✅ Summary

| Feature                | Git                    | Git + LFS                   |
| ---------------------- | ---------------------- | --------------------------- |
| Handles large binaries | ❌ Inefficient          | ✅ Efficient                 |
| Repo size              | Grows with each commit | Only stores pointers in Git |
| Easy to use            | ✅                      | ✅ (after initial setup)     |
| Works with GitHub      | ✅                      | ✅ (requires LFS support)    |

---

## 📚 References

* [Git LFS Documentation](https://git-lfs.github.com/)
* [Git Internals Book (Pro Git)](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain)
* [GitHub Docs: About Git Large File Storage](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)

---

Let me know if you'd like to expand this into a tutorial with screenshots or cover advanced usage (like cleaning LFS history or dealing with CI/CD).
