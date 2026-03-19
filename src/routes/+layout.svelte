<script lang="ts">
	import '$lib/css/variables.css';
	import '$lib/css/styles.css';
	import '$lib/css/utilities.css';
	import { type SchemaOrgProps, SchemaOrg } from 'svead';
	import { utils } from '$lib/scripts/utils';

	const description = utils.getMainDescription();

	const websiteSchema: SchemaOrgProps['schema'] = {
		'@type': 'WebSite',
		name: 'RealPix',
		url: 'https://fab-realpix.netlify.app',
		description
	};

	const orgSchema: SchemaOrgProps['schema'] = {
		'@type': 'Organization',
		name: 'RealPix',
		url: 'https://fab-realpix.netlify.app'
	};
</script>

<SchemaOrg schema={websiteSchema} />
<SchemaOrg schema={orgSchema} />

<slot />
