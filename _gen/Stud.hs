{-# LANGUAGE OverloadedStrings #-}
import Network.HTTP.Simple
import Data.Aeson
import Data.Maybe (fromJust)
import Data.Aeson.Types -- new import for parseMaybe

main :: IO ()
main = do

    response <- getResponseBody <$> httpJSON "http://httpbin.org/get"
    let name = fromJust $ parseMaybe (.: "origin") response :: String

    print name
