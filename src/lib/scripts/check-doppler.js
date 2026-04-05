import { execSync } from 'child_process';

try {
	execSync('doppler --version', { stdio: 'ignore' });
	console.log('Doppler installed...\nMoving forward.');
} catch {
	console.log(
		'Doppler CLI not installed. \nPlease install it from https://docs.doppler.com/docs/install-cli. \nInstall and continue forward.'
	);
	process.exit(1);
}

try {
	execSync('doppler configure get project', { stdio: 'ignore' });
	console.log('Project configured with doppler successfully...\n\nStarting dev server.');
} catch {
	console.log('Running doppler setup from the yaml file....');
	try {
		execSync('doppler setup --no-interactive', { stdio: 'inherit' });
	} catch {
		console.log('Setup failed. Please Run: "doppler setup" to continue forward.');
		process.exit(1);
	}
}
