require 'twitter'
require 'yaml'
require 'json'
require 'active_record'
require 'active_support/all'
require 'getoptlong'
require 'logger'
require 'pidfile'
require_relative 'model/model.rb'
require 'securerandom'
require 'date'

$config_data = YAML.load_file "keys.yml"

$logger = Logger.new(STDOUT)
$logger.level = Logger::INFO

def save_tweet(text,out_file)

	data = {
			text: text, 
			uuid: SecureRandom.uuid,
			source: "twitter",
			created: Date.today
		}

	if !out_file.nil?
		open(out_file,"a") {|f| f << data.to_json ; f << "\n" }
	else
		_tweet = Text.create(data)
	end

	$logger.info "saved text: #{data[:uuid]}"
end

def process_tweet(o, outfile)
	if o.is_a?(Twitter::Tweet) and !o.retweet? and o.lang == 'es' and !o.media? and !o.reply?
		text = o.full_text
		return 0 if o.truncated? #cero ganas de manejar esto
		if o.user_mentions?
			o.user_mentions.each do |m|
				text = text.gsub("@#{m.screen_name}","")
			end
		end
		if o.hashtags?
			o.hashtags.each do |h|
				text = text.gsub("##{h.text}","")
			end
		end
		if o.urls?
			o.urls.each do |u|
				text = text.gsub(u.url,"")
			end
		end
		save_tweet text, outfile
		return 1
	end
	return 0
end

def download_kw(keywords, client, outfile, amt)
	begin
		client.filter(track: keywords.join(",")) do |o|
			break if amt == 0
			amt -= process_tweet o, outfile
		end
	rescue Twitter::Error::TooManyRequests => error
	    sleep error.rate_limit.reset_in + 1
	    retry
	end
end

def download_sample(client, outfile, amt)
	begin
		client.sample do |o|
			break if amt == 0
			amt -= process_tweet o, outfile
		end
	rescue Twitter::Error::TooManyRequests => error
	    sleep error.rate_limit.reset_in + 1
	    retry
	end
end

def download(keywords, out_file, amount)
	stream_client = Twitter::Streaming::Client.new do |config|
		config.consumer_key    = $config_data['consumer_key']
		config.consumer_secret = $config_data['consumer_secret']
		config.access_token 	 = $config_data['access_token']
		config.access_token_secret = $config_data['access_token_secret']
	end

	download_kw stream_keywords, stream_client, out_file, amount if !keywords.nil?
	download_sample stream_client, out_file, amount

end

opts = GetoptLong.new(
	['--keywords','-k',GetoptLong::REQUIRED_ARGUMENT],
	['--json','-j',GetoptLong::REQUIRED_ARGUMENT],
	['--amount','-a',GetoptLong::REQUIRED_ARGUMENT]
	)

keywords = nil
out_file = nil
amount = 100

opts.each do |opt,arg|
	case opt
		when '--keywords'
			keywords = arg.split(',')
		when '--json'
			out_file = arg
		when '--amount'
			amount = arg.to_i
	end
end

#PidFile.new

download keywords, out_file, amount
