package cn.edu.whu.cstar.mosampling.tool;

import java.io.File;
import java.io.FileFilter;
import java.io.IOException;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.filefilter.DirectoryFileFilter;
import org.apache.commons.io.filefilter.FileFileFilter;
import org.apache.commons.io.filefilter.FileFilterUtils;
import org.apache.commons.io.filefilter.IOFileFilter;

public class ApacheFileWrapper {


	public static void copyDirectory(File srcDir, File destDir, String suffix)
	{
		// Create a filter for ".java" files
		IOFileFilter suffixFilter = FileFilterUtils.suffixFileFilter(suffix);
		IOFileFilter suffixFile = FileFilterUtils.and(FileFileFilter.FILE, suffixFilter);
		
		  // Create a filter for either directories or ".java" files
		FileFilter filter = FileFilterUtils.or(DirectoryFileFilter.DIRECTORY, suffixFile);
		
		  // Copy using the filter
		try {
			FileUtils.copyDirectory(srcDir, destDir, filter);
		} catch (IOException e) {
			System.out.println("Error, copying files, for " + srcDir);
			return;
		}
	}
	
	public static void createFolder(File folder)
	{
		try {
			FileUtils.forceMkdir(folder);
		} catch (IOException e) {
			System.out.println("Error, the folder is not created, for  " + folder);
			return;
		}
	}
}
