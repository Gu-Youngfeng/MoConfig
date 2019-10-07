package cn.edu.whu.cstar.mosampling.tool;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

/***
 * <p>Provide the read and write operations for a file.</p>
 * @author jifeng
 * @update 2019.10.5
 */
public class FileReaderWriter {

	/** read lines list from the file in path*/
	public static List<String> readFileByLine(String inPath) {
		BufferedReader inReader = null;
		String line = null;
	
		List<String> result = new ArrayList<String>();
		
		try {
			inReader = new BufferedReader(new FileReader(inPath));
			
			while((line = inReader.readLine()) != null)
			{
				result.add(line);
			}
			
			inReader.close();
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return result;
	}
	
	public static boolean writeFileByLine(String outPath, List<String> listLine) {
		boolean res = false;
		
		PrintWriter outWriter = null;
		String line = null;
		
		try {
			outWriter = new PrintWriter(new FileWriter(outPath));
			
			int size = listLine.size();
			for(int i = 0; i < size; i ++)
			{
				line = listLine.get(i);
				outWriter.println(line);
			}
			
			outWriter.close();
			res = true;
			
		} catch (IOException e) {
			e.printStackTrace();
			res = false;
		}
		
		return res;
	}
	
	
}
