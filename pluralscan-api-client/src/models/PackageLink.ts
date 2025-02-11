export type PackageLinkLabel = 'SourceRepository' | ''

export interface PackageLink {
    label: PackageLinkLabel;
    url: string;
}