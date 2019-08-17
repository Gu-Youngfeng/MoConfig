package cn.edu.whu.cstar.mosampling.moea;

import java.util.List;

import cn.edu.whu.cstar.mosampling.tool.FileReaderWriter;

/***
 * <p>Class MOEAInstance reads the 2-dimension array from .csv file.</p> 
 */
public class MOEAInstance {

	/* i - one configuration, j - one option */
	double[][] matrixValue = null; // save all the configuration into the 2-dimension array, matrixValue
	
	
	int numOption = 8; // number of options
	int numConfiguration = -1; // number of configurations
	
	
	public MOEAInstance(String inPath)
	{
		readInstance(inPath);
	}
	
	public void readInstance(String inPath)
	{
		List<String> listLine = FileReaderWriter.readFileByLine(inPath);
		numConfiguration = listLine.size() -1; // assignment of numConfiguration
		
		String line = null;
		double value = -1;
		
		line = listLine.get(0); // the 1st line in .csv file presents the option name and performance name
		String[] arrayToken = line.split(",");
		numOption = arrayToken.length -1; // assignment of numOption
		
		matrixValue = new double[numConfiguration][numOption]; // save all the configuration into the 2-dimension array, matrixValue
		
		for(int i = 1; i < numConfiguration; i ++)
		{
			line = listLine.get(i);
			arrayToken = line.split(",");
			
			for(int j = 0; j < numOption; j ++)
			{
				String token = arrayToken[j];
				value = Double.parseDouble(token);
				matrixValue[i][j] = value;
			}
		}	
	}
}