<script lang="ts">
	import { resolve } from '$app/paths';
</script>

<svelte:head>
	<title>Home</title>
</svelte:head>

<p>Hello</p>
<a href={resolve('/imageUpload')}>Image</a>
