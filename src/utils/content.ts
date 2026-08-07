export interface ContentFrontmatter {
	title: string;
	date: string;
	category?: string;
	description?: string;
}

export interface ContentEntry {
	url: string;
	frontmatter: ContentFrontmatter;
}

type GlobModules = Record<string, { url?: string; frontmatter: ContentFrontmatter }>;

export function sortByDateDesc(modules: GlobModules): ContentEntry[] {
	return Object.values(modules)
		.filter((mod): mod is { url: string; frontmatter: ContentFrontmatter } => Boolean(mod.url))
		.map((mod) => ({ url: mod.url, frontmatter: mod.frontmatter }))
		.sort((a, b) => new Date(b.frontmatter.date).getTime() - new Date(a.frontmatter.date).getTime());
}
