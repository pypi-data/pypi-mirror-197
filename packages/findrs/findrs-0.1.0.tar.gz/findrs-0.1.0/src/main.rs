use std::ffi::OsStr;
use std::path::PathBuf;

use clap::Parser;
use walkdir::WalkDir;

#[derive(Debug, Parser)]
#[command(about = "Find all files containing a given name.")]
pub struct Arguments {
	/// Name to find. // (4) ! 
	#[arg(short, long)]
	pub name: String,
	/// Path to check.
	#[arg(default_value = ".")]
	pub path: PathBuf,
}

fn main() {
	let args = Arguments::parse();
	
	for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
		let path = entry.path();
		if path.is_file() {
			match &path.file_name().and_then(OsStr::to_str) {
				Some(name) if name.contains(&args.name) => println!("{}", path.display()), _ => (),
			}
		}
	}
}
