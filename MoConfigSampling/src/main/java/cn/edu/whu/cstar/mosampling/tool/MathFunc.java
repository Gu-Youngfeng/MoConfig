package cn.edu.whu.cstar.mosampling.tool;

import java.math.BigDecimal;

public class MathFunc {

	public static double roundDoubleValue(double value, int bit)
	{
		BigDecimal decimal = new BigDecimal(value);  
		return decimal.setScale(bit, BigDecimal.ROUND_HALF_UP).doubleValue();  
	}
}
