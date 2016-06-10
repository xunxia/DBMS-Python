module Main where

import System.IO
import Data.List
import Data.List.Split

--delete "|"
delSepe ::[String]->[[String]]
delSepe infoList = map (splitOn "|") infoList

--orderDB: put the same order number together
gatherItem::[[String]]->[String]->[String]
gatherItem orderList currentList = nub ((init currentList)++(foldl (\acc x->if x!!1 == currentList!!1 then (x!!3):acc else acc) [] orderList))

gatherItemAll orderList = nub (map (gatherItem orderList) orderList)

--filter the custDB based on age
seniorCust custList = filter (\x-> (x!!2)>="60") custList

filSales salesList senCustEle= map (\m->(senCustEle!!1):m) (filter (\s -> s!!1 == senCustEle!!0) salesList)

seniorSales senCust salesList= concatMap (filSales salesList) senCust 

filItem orderList senSaleEle = map (\m->(senSaleEle!!0):(senSaleEle!!1):(senSaleEle!!3):(m!!1):[]) (filter (\s->s!!0 == senSaleEle!!1) orderList)
seniorItem senSale orderList = concatMap (filItem orderList) senSale

--to show the report
itemStr :: [String] -> [String]
itemStr ele = (fst eleTup) ++ [intercalate "," (snd eleTup)]
        where eleTup = (splitAt 3 ele)
        
itemShowAll :: [[String]]->[[String]]
itemShowAll item = ["Customer", "Order#", "Date", "Items"]:(map itemStr item)

blankNum l s= concat (take num (repeat " "))
        where num = l - length(s)

addBlank l sList = (sList!!0)++(blankNum l (sList!!0))++(sList!!1)++(blankNum (l-5) (sList!!1) )++(sList!!2)++(blankNum (l-3) (sList!!2) )++(sList!!3)       
--addBlank l sList = intercalate "  " (map (\s->s++(blankNum l s)) sList)

showResult result l = map (addBlank l) (itemShowAll result)

main::IO()
main = do
        contentSales<- readFile "SalesDB.slc.txt"
        contentOrder<- readFile "OrderDB.slc.txt"
        contentCust<- readFile "CustDB.slc.txt"

        let orderList = delSepe (lines contentOrder)
        
        let custList = delSepe (lines contentCust)
        let filterCust = seniorCust custList
        
        let salesList = delSepe (lines contentSales)
        let filterSale = seniorSales filterCust salesList
        
        let filterItem = seniorItem filterSale orderList
        let gatherOr = gatherItemAll filterItem--filter first, then gather items.
        
        let showValue = showResult gatherOr 20
        putStrLn $ unlines showValue