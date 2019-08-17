
package cn.edu.whu.cstar.mosampling.tool;


import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class RandomFunc {

	private final static int LARGE_NUM_RANDOM = 65536; 
	
	private static Random randomOperator = null;
	
	public static void init()
	{
		if(randomOperator == null)
			randomOperator = new Random(System.currentTimeMillis());
	}
	
	public static int nextInt(int max) //max is exclusive
	{
		return randomOperator.nextInt(max);
	}
	
	public static int nextInt(int min, int max) //min is inclusive and max is exclusive
	{
		return randomOperator.nextInt(max - min) + min;
	}
	
	public static void nextBytes(byte[] arrayByte) 
	{
		randomOperator.nextBytes(arrayByte);
	}

	public static float nextFloat()
	{
		return randomOperator.nextFloat();
	}
	
	public static double nextDouble()
	{
		return randomOperator.nextDouble();
	}
	
	
	public static boolean isProbabilitySatisfied(double p)
	{
		if(p == 1.0)
			return true;
		
		return randomOperator.nextInt(LARGE_NUM_RANDOM) < p * LARGE_NUM_RANDOM;
	}
	
	public static int nextElement(List<Integer> list)
	{
		int size = list.size();
		if(size == 0)
		{
			System.out.println("Error, empty list.");
			return -1;
		}
		else if(size == 1)
			return list.get(0);
		
		return list.get(nextInt(size));
	}
	
	public static List<Integer> removeElements(List<Integer> list, int numRemoval)
	{
		int size = list.size();
		
		boolean[] arrayMask = new boolean[size];
		for(int k = 0; k < size; k ++)
			arrayMask[k] = false;
		int index = -1;
		
		int counter = 0;
		while(counter < numRemoval)
		{
			index = nextInt(size);
			if(! arrayMask[index])
			{
				arrayMask[index] = true;
				counter ++;
			}
		}
		
		List<Integer> listRes = new ArrayList<Integer>();
		for(int k = 0; k < size; k ++)
			if(! arrayMask[k])
				listRes.add(list.get(k));
		
		return listRes;
	}
	
	
	/**
	 * Return a set with {@code numSelected} elements. This set is a sub set of {0, 1, ..., size -1}. 
	 * @param size
	 * @param numSelected
	 * @return
	 */
	public static List<Integer> selectElements(int size, int numSelected)
	{
		List<Integer> listRes = new ArrayList<Integer>();
		if(size == 0)
			return  listRes;
		
		if(numSelected >= size)
		{
			for(int i = 0; i < size; i ++)
				listRes.add(i);
			return listRes;
		}
		else if(numSelected <= 0)
			return listRes;
		
		boolean[] arrayMask = new boolean[size];
		for(int k = 0; k < size; k ++)
			arrayMask[k] = false;
		int index = -1;
		
		int counter = 0;
		while(counter < numSelected)
		{
			index = nextInt(size);
			if(! arrayMask[index])
			{
				arrayMask[index] = true;
				counter ++;
			}
		}
		
		for(int k = 0; k < size; k ++)
			if(arrayMask[k])
				listRes.add(k);
		
		return listRes;
	}
	
}
