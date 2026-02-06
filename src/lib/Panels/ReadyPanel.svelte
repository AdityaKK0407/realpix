<script lang="ts">
	import { get } from "svelte/store";
	import { uploadedFiles } from '../../routes/(shared-header)/imageUpload/stores/uploadFlow.store';
	import { onDestroy } from 'svelte';

	interface Props {
		fileType: 'image' | 'video'
	}

	const files = get(uploadedFiles)
	const index = $state(0)
	const props: Props = $props()
	const typeFiles = files.filter(file => {
		if(file.type === props.fileType)
			return true
	})
	const urls = typeFiles.map(file => URL.createObjectURL(file.src))
	const selectedImage = $derived(urls[index])

	onDestroy(() => {
		urls.forEach(url => URL.revokeObjectURL(url))
	})
</script>

<section class="ready-container">
	<section class="image-container">
		<img src={selectedImage} alt="Image" aria-hidden="true"/>
	</section>
	<section>

	</section>
</section>

<style>
	section {
			flex-grow: 1;
	}

	.image-container {
			display: flex;
			min-height: 250px;
			max-height: 325px;
			width: 100%;
	}

	img {
			max-width: 100%;
			max-height: 100%;
			width: auto;
			height: auto;
			object-fit: contain;
			display: block;
	}
</style>