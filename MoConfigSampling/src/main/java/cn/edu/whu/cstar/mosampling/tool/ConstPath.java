package cn.edu.whu.cstar.mosampling.tool;

import java.io.File;

public class ConstPath {

//	private final static String PATH_METADATA = ".metadata";
	public final static String PATH_SEPARATOR = File.separator;	// / or \
	public final static String PATH_UNION = File.pathSeparator;	// : 
	
	public final static char CHAR_SEPARATOR = File.separator.charAt(0);	// / or \
	public final static String PATH_SUFFIX_JAVA = ".java";
	public final static String PATH_SUBCLASS_JAVA = "$";	
	
	public final static String PATH_NEXTLINE = System.getProperty("line.separator");
	public final static String PATH_PROJECT_ROOT = System.getProperty("user.dir");
	
	public final static String PATH_DEFAULT_OUTPUT_FOLDER_SPOON = "spooned";
	public final static String PATH_DEFAULT_OUTPUT_FOLDER_COMPILER = "compiled";
	
	
	public final static String CONFIG_SPLIT = "\\|";
	public final static String CONFIG_DEFAULT = ".";
}
