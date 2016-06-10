module Main where

import Data.List.Split
import System.IO
import Data.List
import Data.Function
import Numeric

--delete "|"
delSepe ::[String]->[[String]]
delSepe infoList = map (splitOn "|") infoList 

--get cust and total, it only for one line
getInfo ::[String]->[String]
getInfo [_,a,_,b] = [a,b]

--convert String to Float type, it is only for one line
strToFloat::[String]->[Float]
strToFloat = map read

--convert all lines into the [cust, total] and in Float type
--conTypeConv ::[String]->[[Float]]
conTypeConv info = map strToFloat (map getInfo (delSepe info))

--calculate the total of one cust
--eleAcc::[[String]]->[String]-> [String]
totalCal infoListL currentList = (currentList!!0): (foldl (\acc x-> if x!!0 == currentList!!0 then acc+(x!!1) else acc) 0 infoListL):[]

--calculate all lines and delete the duplicate. 
reportValue infoListL = nub (map (totalCal infoListL) infoListL)

--sort the reportValue
sortedReport infoList = sort (reportValue infoList)

--change the float type to string type of one line
showEle eleList = show(round(eleList!!0)): (showGFloat (Just 2) (eleList!!1) ""):[]

--calculate how many blank should Be add between cust and total
--blankNum::Int->String
blankNum s l = concat (take num (repeat " "))
        where num = length("Cust")-length(s!!0)+l

--add blank for one line        
addBlank l s= (s!!0)++(blankNum s l)++(s!!1)

--add the title
showResult result = ["Cust","Sales"]:(map showEle result)

--final show format without seperate lines.
finalShow result l = map (addBlank l) (showResult result)


main::IO()
main = do        
        handle<- openFile "SalesDB.slc.txt" ReadMode
        contents <- hGetContents handle
        let conList = lines contents
        let convertCont = conTypeConv conList
        --print convertCont
        let sortedRep = sortedReport convertCont
        let finalR = finalShow sortedRep 10
        putStrLn "The report of SalesDB is as below."
        putStrLn $ unlines finalR
        

        
        
