<script lang="ts">
	import FileUpload from '$lib/Components/FileUpload.svelte';
	import { type FileType, uploadData } from '$lib/state/uploadFlow.store';
	import { transition, uploadState } from '$lib/upload/upload.store';
	import Reset from '$lib/Panels/Reset.svelte';
	import ReadyPanel from '$lib/Panels/ReadyPanel.svelte';
	import { Panel } from '$lib/types/Panel';
	import UploadingPanel from '$lib/Panels/UploadingPanel.svelte';

	function setFiles(newFiles: File[], fileType: FileType) {
		uploadData.uploadFiles(newFiles, fileType);
		transition('SELECT_IMAGE');
		activePanel = Panel.Processing_Panel;
	}

	function setClassNames(panelNo: Panel) {
		return activePanel === panelNo ? 'active-layout' : 'inactive-layout';
	}

	let activePanel: Panel = $state(Panel.Uploading_Panel);
</script>

<svelte:head>
	<title>Image Upload</title>
	<meta
		name="description"
		content="Upload up to 5 images to detect deepfakes and verify authentication. Instant AI-powered analysis with detailed results. Your images are encrypted and deleted after processing"
	/>

	<meta
		name="keywords"
		content="upload image for verification, check photo authenticity, upload picture to detect fake, analyze image for deepfake, verify photo online, image upload deepfake detection"
	/>

	<meta property="org:type" content="website" />
	<meta property="og:url" content="https://fab-realpix.netlify.app/imageUpload" />
	<meta
		property="og:title"
		content="Upload images to instantly detect deepfakes with AI analysis. Secure and encrypted."
	/>
	<meta
		property="og:description"
		content="Detect deepfakes and verify the authenticity of images instantly with AI powered analysis to identify manipulated images."
	/>

	<meta property="twitter:card" content="summary_large_image" />
	<meta property="twitter:url" content="https://fab-realpix.netlify.app/imageUpload" />
	<meta
		property="twitter:title"
		content="Upload images to instantly detect deepfakes with AI analysis. Secure and encrypted."
	/>
	<meta
		property="twitter:description"
		content="Detect deepfakes and verify the authenticity of images instantly with AI powered analysis to identify manipulated images."
	/>

	<script type="application/ld+json">
		{
			"@context": "https://schema.org/",
			"@type": "WebPage",
			"name": "Upload Images for Deepfake Detection",
			"url": "https://fab-realpix.netlify.app/imageUpload",
			"description": "Upload and analyze images to detect deepfakes and verify authenticity"
		}
	</script>
</svelte:head>

<main>
	<section class={setClassNames(Panel.Uploading_Panel)} class:items-center={true}>
		<FileUpload onSelect={setFiles} extensions="PNG, JPG, JPEG" fileType="image" />
	</section>
	<section class={setClassNames(Panel.Processing_Panel)} class:relative={true}>
		{#if $uploadState === 'idle'}
			<Reset text={['Upload images to begin analyzing', 'for authenticity']} />
		{:else if $uploadState === 'ready'}
			<ReadyPanel fileType="image" />
		{:else if $uploadState === 'uploading'}
			<UploadingPanel fileType="image" />
		{/if}
	</section>
</main>

<style>
	main {
		display: grid;
		grid-template-columns: 0.32fr 0.68fr;
		gap: var(--layout-panel-gap);
		transition: grid-template-columns 500ms ease-in-out;
	}

	section {
		background-color: var(--color-bg-surface);
		border-radius: var(--layout-panel-rounded);
		padding-inline: var(--app-padding-inline);
		padding-block: var(--app-padding-block);
		transition: filter 400ms ease-in-out;
		display: flex;
	}
</style>
