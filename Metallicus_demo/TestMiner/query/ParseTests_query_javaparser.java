import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.expr.CastExpr;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

/*
 * Parses test suite of query to get test array from it
 * Soot can't be used as src missing
 * #TODO: integrate with param matching script for sim score computation
 */
public class ParseTests_query_javaparser  {

    public static void main(String[] args) {
    	//takes arg0 as path where to search query src, arg1: name of query file, arg2: signature
    	//args[0]="D:/Desktop/PA/PAworkspace/JavaParser_sample/src";
    	File projectDir = new File(args[0]);
    	//args[1]="HelloWorld.java";
    	ArrayList super_list=new ArrayList<>();//outermost list containing list of val,arg,type to be processed
    	ArrayList<String[]> arg_type_pairs=getarg_typ(args[2]);
    	new DirExplorer((level, path, file) -> path.endsWith(args[1]), (level, path, file) -> {
        	    	
            try {
                new VoidVisitorAdapter<Object>() {
                    @Override
                    public void visit(MethodCallExpr call, Object arg) {
                        super.visit(call, arg);
                        if(call.getNameAsString().equals("assertEquals"))
                        { ArrayList tuples_list=new ArrayList<>();
                        	NodeList<Expression> args=call.getArguments();
                        	//segregate expected and inputs. check for list/collection type args
                        	boolean flag=false;//to track if expected value captured- first one is assumed
                        	for (Expression a:args)
                        	{	if(a instanceof MethodCallExpr)//for target method args
                        		{ int arg_ctr=0;
                        			
                        			//System.out.println(((MethodCallExpr) a).getArguments());
                        			for(Expression a_child:a.asMethodCallExpr().getArguments())
                        			{	ArrayList<String> tuple=new ArrayList<String>();
                            			if(a_child instanceof CastExpr)
                        					tuple.add("'"+a_child.asCastExpr().getExpression().toString()+"'");
                        				else
                        					tuple.add("'"+a_child.toString()+"'");
                            			String[] arg_type=arg_type_pairs.get(arg_ctr);
                        				tuple.add("'"+arg_type[0]+"'");//arg name
                        				tuple.add("'java_"+arg_type[1]+"'");//argtype assumes given in canonical form e.g. String and not java.lang.String
                        				tuples_list.add(tuple);
                        				arg_ctr++;
                        			}
                        			
                        		}
                        		else if(a instanceof CastExpr && !flag)//expected value
                        		{	ArrayList<String> tuple=new ArrayList<String>();
                        			flag=true;
                        			tuple.add("'"+a.asCastExpr().getExpression().toString()+"'");
                    				tuple.add("'EXP_op'");//arg name
                    				tuple.add("'java_"+getExpValType(a)+"'");//argtype
                    				tuples_list.add(tuple);
                        			
                        		}
                        		else//expected value
                        		{
                        			if(!flag)
                        			{	ArrayList<String> tuple=new ArrayList<String>();
                            		
                        				flag=true;
                        				tuple.add("'"+a.toString()+"'");
                        				tuple.add("'EXP_op'");//arg name
                        				tuple.add("'java_"+getExpValType(a)+"'");//argtype
                        				tuples_list.add(tuple);
                            		}	
                        		}
                        	}
                        	super_list.add(tuples_list);
                        }
                       }
                }.visit(StaticJavaParser.parse(file), null);
            } catch (IOException e) {
                new RuntimeException(e);
            }
/*            try {
				Files.write(Paths.get("docs.json"), content_to_write.getBytes(), StandardOpenOption.APPEND);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
*/            }).explore(projectDir);
    	System.out.println(super_list);
        
    }

    // extract argname and type- returns pairs of name,type- arraylist of String[] containing a pair
   public static ArrayList getarg_typ(String signature)
   {
	   ArrayList<String[]> arr=new ArrayList<String[]>();
	   ArrayList<Integer> commas=new ArrayList<Integer>();
	   boolean flag=false;// to track if in '<>'
	   int ctr=0;
	   //System.out.println(signature);
	   String args_region=signature.substring(signature.indexOf('(')+1);
		 
	   for(char c: args_region.toCharArray())
	   {
		   if(c=='<')
			   flag=true;
		   else if (c=='>')
			   flag=false;
		   else if (c==',' && !flag)
			   commas.add(ctr);   

		   ctr=ctr+1;
	   }
	   if(!args_region.endsWith("()"))
		   commas.add(args_region.lastIndexOf(')'));
	   int indx=0;
	   //System.out.println(commas);
	   for(int i:commas)
	   {
		   String type_arg=args_region.substring(indx,i);
		   String type=type_arg.substring(0,type_arg.lastIndexOf(" "));
		   String arg=type_arg.substring(type_arg.lastIndexOf(" ")+1);
		   String[] pair={arg.trim(),type.trim()};
		   arr.add(pair);
		   indx=i+1;
	   }
   return arr;
	   
   }
   
   static String getExpValType(Expression e)
   {
	   if(e.isBooleanLiteralExpr())
		   return "boolean";
	   else if(e.isCharLiteralExpr())
		   return "char";
	   else if(e.isDoubleLiteralExpr())
		   return "double";
	   else if(e.isIntegerLiteralExpr())
		   return "int";
	   else if (e.isLongLiteralExpr())
		   return "long";
	   else if (e.isStringLiteralExpr())
		   return "String";
	   else
		   return "";
   
   }
}
