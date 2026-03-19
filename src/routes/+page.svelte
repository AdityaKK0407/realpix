<script lang="ts">
	import { resolve } from '$app/paths';
	import { PUBLIC_WEBSITE_URL } from '$env/static/public';
	import { utils } from '$lib/scripts/utils';
	import { Head, SchemaOrg } from 'svead';
	import type { SchemaOrgProps, SeoConfig } from 'svead';

	const description = utils.getMainDescription();

	const seo_config: SeoConfig = {
		title: 'RealPix - AI Image Deepfake Detector',
		description: description,
		url: PUBLIC_WEBSITE_URL,
		website: PUBLIC_WEBSITE_URL,
		author_name: 'Team Fabulous',
		site_name: 'RealPix'
	};

	const schemaOrg: SchemaOrgProps['schema'] = {
		'@type': 'SoftwareApplication',
		name: 'RealPix',
		url: PUBLIC_WEBSITE_URL,
		description: description,
		applicationCategory: 'UtilitiesApplication',
		operatingSystem: 'Any',
		offers: {
			price: '0',
			priceCurrency: 'USD',
			'@type': 'Offer'
		}
	};
</script>

<Head {seo_config} />
<SchemaOrg schema={schemaOrg} />
<section>
	<header>
		<h1>RealPix</h1>
	</header>
	<main>
		<p>Hello</p>
		<a href={resolve('/imageUpload')}>Image</a>
	</main>
</section>

<style>
	header {
		grid-row-start: 1;
	}
</style>
