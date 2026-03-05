<script lang="ts">
	import axios from 'axios';
	import { type FileType, uploadData } from '$lib/state/uploadFlow.store';
	import { addSBasedOnCondition } from '$lib/scripts/utils';

	interface Props {
		fileType: FileType;
	}

	const props: Props = $props();
	let progress = $state(0);
	const data = uploadData.getFileType(props.fileType);

	async function upload() {
		if (data) {
			const formData = new FormData();
			const fileType = props.fileType;
			data.forEach((data) => {
				formData.append(addSBasedOnCondition(true, props.fileType), data.src);
			});

			try {
				await axios.post('/api/uploadImage', formData, {
					onUploadProgress: (event) => {
						if (event && event.total) {
							const percent = Math.round((event.loaded * 100) / event.total);
							progress = percent;
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
	<p>Uploaded: {progress}</p>
</section>

<style>
	.uploading__container {
		flex-grow: 1;
	}
</style>
