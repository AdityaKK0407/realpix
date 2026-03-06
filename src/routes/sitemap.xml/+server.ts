export const GET = async () => {
	const baseUrl = 'https://fab-realpix.netlify.app';
	const pages = [
		{ url: '', priority: '0.6', changefreq: 'monthly' },
		{ url: 'imageUpload', priority: '1.0', changefreq: 'daily' }
	];

	const siteMap = `<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            ${pages
							.map(
								(page) => `
                <url>
                    <loc>${baseUrl}/${page.url}</loc>
                    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
                    <changefreq>${page.changefreq}</changefreq>
                    <priority>${page.priority}</priority>
                </url>
            `
							)
							.join('\n')}
        </urlset>
    `;

	return new Response(siteMap, {
		headers: {
			'Content-Type': 'application/xml',
			'Cache-Control': 'max-age=3600'
		}
	});
};
