<script lang="ts">
	import { get } from "svelte/store";
	import { uploadedFiles } from '../../routes/(shared-header)/imageUpload/stores/uploadFlow.store';
	import { onDestroy } from 'svelte';

	const files = get(uploadedFiles)
	const index = $state(0)
	const urls = files.map(file => URL.createObjectURL(file))
	const selectedImage = $derived(urls[index])
	console.log(selectedImage)

	onDestroy(() => {
		urls.forEach(url => URL.revokeObjectURL(url))
	})
</script>

<section class="ready-container">
	<section class="image-container">
		<img src={selectedImage} alt="Image" aria-hidden="true"/>/
	</section>
	<section></section>
</section>

<style>
	section {
			flex-grow: 1;
	}

	.ready-container {
			display: grid;
			grid-template-columns: 0.7fr 0.3fr;
	}

	img {
			aspect-ratio: 1 / 1;
	}
</style>