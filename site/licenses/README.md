# Prebundled runtime notices

`@pagefind/default-ui` ships precompiled Svelte and language-tag helpers. Its
package declares Svelte `^4.2.1` but does not identify the embedded patch release.
The generated notices identify the distributed UI artifact by SHA-256; they do
not infer the embedded version from an unrelated installation.

The Svelte notice is preserved from the official Svelte 4.2.20 license:
https://raw.githubusercontent.com/sveltejs/svelte/svelte%404.2.20/LICENSE.md
This is a license-text reference, not a claim about the embedded patch version.

Other notices are read from the corresponding installed public package license
files. Vite supplies the actual client-bundle package inventory. Pagefind's
copied runtime receives the notices shipped with its installed distribution.
