<script lang="ts">
	import axios from 'axios';
	import { writable } from 'svelte/store';
	import { type FileType, uploadData } from '$lib/state/uploadFlow.store';

	interface Props {
		fileType: FileType;
	}

	const props: Props = $props();
	const progress = writable(0);
	const data = uploadData.getFileType(props.fileType);

	async function upload() {
		if (data) {
			const formData = new FormData();
			const fileType = props.fileType;
			data.forEach((data) => {
				formData.append(fileType, data.blob);
			});

			try {
				await axios.post('/api', formData, {
					headers: { 'Content-Type': 'multipart/form-data' },
					onUploadProgress: (event) => {
						if (event && event.total) {
							const percent = Math.round((event.loaded * 100) / event.total);
							progress.set(percent);
						}
					}
				});
			} catch (err) {
				alert(`Error occured: ${err}`);
			}
		}
	}

	upload();
</script>

<section class="uploading__container">
	<p>Uploaded: {$progress}</p>
</section>

<style>
	.uploading__container {
		flex-grow: 1;
	}
</style>
